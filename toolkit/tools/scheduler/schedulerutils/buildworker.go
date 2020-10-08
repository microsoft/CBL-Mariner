// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"
	"time"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/retry"
	"microsoft.com/pkggen/scheduler/buildagents"
)

// BuildChannels represents the communicate channels used by a build agent.
type BuildChannels struct {
	Requests <-chan *BuildRequest
	Results  chan<- *BuildResult
	Cancel   <-chan struct{}
}

// BuildRequest represents the results of a build agent trying to build a given node.
type BuildRequest struct {
	Node           *pkggraph.PkgNode
	PkgGraph       *pkggraph.PkgGraph
	AncillaryNodes []*pkggraph.PkgNode
	CanUseCache    bool
}

// BuildResult represents the results of a build agent trying to build a given node.
type BuildResult struct {
	Err            error
	LogFile        string
	Node           *pkggraph.PkgNode
	AncillaryNodes []*pkggraph.PkgNode
	UsedCache      bool
	BuiltFiles     []string
}

// BuildNodeWorker process all build requests, can be run concurrently with multiple instances.
func BuildNodeWorker(channels *BuildChannels, agent buildagents.BuildAgent, buildAttempts int) {
	for req := range channels.Requests {
		select {
		case <-channels.Cancel:
			logger.Log.Warn("Cancellation signal received")
			return
		default:
		}

		res := &BuildResult{
			Node:           req.Node,
			AncillaryNodes: req.AncillaryNodes,
		}

		switch req.Node.Type {
		case pkggraph.TypeBuild:
			res.UsedCache, res.BuiltFiles, res.LogFile, res.Err = buildBuildNode(req.Node, req.PkgGraph, agent, req.CanUseCache, buildAttempts)
			if res.Err == nil {
				for _, node := range req.AncillaryNodes {
					if node.Type == pkggraph.TypeBuild {
						node.State = pkggraph.StateUpToDate
					}
				}
			}

		case pkggraph.TypeRun, pkggraph.TypeGoal, pkggraph.TypeRemote, pkggraph.TypePureMeta:
			res.UsedCache = req.CanUseCache

		case pkggraph.TypeUnknown:
			fallthrough

		default:
			res.Err = fmt.Errorf("invalid node type %v on node %v", req.Node.Type, req.Node)
		}

		channels.Results <- res
	}

	logger.Log.Debug("Worker done")
}

// buildBuildNode builds a TypeBuild node, either used a cached copy if possible or building the corresponding SRPM.
func buildBuildNode(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, agent buildagents.BuildAgent, canUseCache bool, buildAttempts int) (usedCache bool, builtFiles []string, logFile string, err error) {
	cfg := agent.Config()

	baseSrpmName := filepath.Base(node.SrpmPath)
	if canUseCache {
		usedCache, builtFiles = isSRPMPrebuilt(node.SpecPath, cfg.RpmDir, node.SourceDir, cfg.DistTag)
		if usedCache {
			logger.Log.Debugf("%s is prebuilt, skipping", baseSrpmName)
			return
		}
	}

	// get all build dependencies
	dependencyLookup := make(map[string]bool)

	search := traverse.BreadthFirst{}
	search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
		dependencyNode := n.(*pkggraph.PkgNode)

		if dependencyNode.State == pkggraph.StateCached {
			dependencyName := dependencyNode.VersionedPkg.Name
			// Encode any version specific information into the dependency.
			// Use the same logic as the fetchers.
			switch dependencyNode.VersionedPkg.Condition {
			// Not supported, request any version
			case "<":

			// Treat <= as =
			case "<=", "=":
				dependencyName = fmt.Sprintf("%s-%s", dependencyName, dependencyNode.VersionedPkg.Version)

			// Treat > and >= as "latest"
			case ">", ">=":
			default:
			}

			dependencyLookup[dependencyName] = true

			return
		}

		rpmPath := dependencyNode.RpmPath
		if rpmPath == "" || rpmPath == "<NO_RPM_PATH>" || rpmPath == node.RpmPath {
			return
		}

		dependencyLookup[rpmPath] = true

		return
	})

	dependencies := make([]string, 0, len(dependencyLookup))
	for depName := range dependencyLookup {
		dependencies = append(dependencies, depName)
	}

	logger.Log.Infof("Building %s", baseSrpmName)
	builtFiles, logFile, err = buildSRPMFile(agent, buildAttempts, node.SrpmPath, dependencies)
	return
}

// buildSRPMFile sends an SRPM to a build agent to build.
func buildSRPMFile(agent buildagents.BuildAgent, buildAttempts int, srpmFile string, dependencies []string) (builtFiles []string, logFile string, err error) {
	const (
		retryDuration = time.Second
	)

	logBaseName := filepath.Base(srpmFile) + ".log"
	err = retry.Run(func() (buildErr error) {
		builtFiles, logFile, buildErr = agent.BuildPackage(srpmFile, logBaseName, dependencies)
		return
	}, buildAttempts, retryDuration)

	return
}
