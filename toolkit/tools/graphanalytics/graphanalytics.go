// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"
	"path/filepath"
	"sort"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"
	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/sliceutils"
)

const (
	defaultMaxResults = "10"
)

// mapPair represents a key/value pair in a map[string][]string.
// What the key and value represent are defined by the functions that use this.
type mapPair struct {
	key   string
	value []string
}

var (
	app            = kingpin.New("graphanalytics", "A tool to print analytics of a given dependency graph.")
	inputGraphFile = exe.InputFlag(app, "Path to the DOT graph file to analyze.")
	maxResults     = app.Flag("max-results", "The number of results to print per catagory. Set 0 to print unlimited.").Default(defaultMaxResults).Int()
	logFile        = exe.LogFileFlag(app)
	logLevel       = exe.LogLevelFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)

	err := analyzeGraph(*inputGraphFile, *maxResults)
	if err != nil {
		logger.Log.Fatalf("Unable to analyze dependency graph, error: %s", err)
	}
}

// analyzeGraph analyzes and prints various attributes of a graph file.
func analyzeGraph(inputFile string, maxResults int) (err error) {
	pkgGraph := pkggraph.NewPkgGraph()
	err = pkggraph.ReadDOTGraphFile(pkgGraph, inputFile)
	if err != nil {
		return
	}

	printDirectlyMostUnresolved(pkgGraph, maxResults)
	printDirectlyClosestToBeingUnblocked(pkgGraph, maxResults)

	printIndirectlyMostUnresolved(pkgGraph, maxResults)
	printIndirectlyClosestToBeingUnblocked(pkgGraph, maxResults)

	return
}

func printIndirectlyMostUnresolved(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	unresolvedPackageDependents := make(map[string][]string)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeRun && node.Type != pkggraph.TypeBuild {
			continue
		}

		if node.State == pkggraph.StateUnresolved {
			continue
		}

		dependentName := nodeDependencyName(node)

		search := traverse.BreadthFirst{}
		search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
			dependencyNode := n.(*pkggraph.PkgNode)

			if dependencyNode.State != pkggraph.StateUnresolved {
				return
			}

			unresolvedPkgName := dependencyNode.VersionedPkg.Name
			insertIfMissing(unresolvedPackageDependents, unresolvedPkgName, dependentName)

			return
		})
	}

	printTitle("[INDIRECT] Most common unresolved dependencies")
	printMap(unresolvedPackageDependents, "total dependents", maxResults)

	return
}

func printDirectlyMostUnresolved(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	unresolvedPackageDependents := make(map[string][]string)

	for _, node := range pkgGraph.AllRunNodes() {
		if node.State != pkggraph.StateUnresolved {
			continue
		}

		pkgName := node.VersionedPkg.Name

		dependents := pkgGraph.To(node.ID())
		for dependents.Next() {
			dependent := dependents.Node().(*pkggraph.PkgNode)
			if dependent.Type == pkggraph.TypeGoal {
				continue
			}

			dependentName := nodeDependencyName(dependent)
			insertIfMissing(unresolvedPackageDependents, pkgName, dependentName)
		}
	}

	printTitle("[DIRECT] Most common unresolved dependencies")
	printMap(unresolvedPackageDependents, "direct dependents", maxResults)

	return
}

func printDirectlyClosestToBeingUnblocked(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	srpmsBlockedBy := make(map[string][]string)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeBuild {
			continue
		}

		if node.State == pkggraph.StateUnresolved {
			continue
		}

		pkgSRPM := filepath.Base(node.SrpmPath)

		dependencies := pkgGraph.From(node.ID())
		for dependencies.Next() {
			dependency := dependencies.Node().(*pkggraph.PkgNode)
			if dependency.State != pkggraph.StateBuild && dependency.State != pkggraph.StateUnresolved {
				continue
			}

			dependencySRPM := filepath.Base(dependency.SrpmPath)
			if pkgSRPM == dependencySRPM {
				continue
			}

			dependencyName := nodeDependencyName(dependency)
			insertIfMissing(srpmsBlockedBy, pkgSRPM, dependencyName)
		}
	}

	printTitle("[DIRECT] SRPMs closest to being ready to build")
	printReversedMap(srpmsBlockedBy, "unmet dependencies", maxResults)
}

func printIndirectlyClosestToBeingUnblocked(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	srpmsBlockedBy := make(map[string][]string)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeBuild {
			continue
		}

		if node.State == pkggraph.StateUnresolved {
			continue
		}

		pkgSRPM := filepath.Base(node.SrpmPath)

		search := traverse.BreadthFirst{}
		search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
			dependency := n.(*pkggraph.PkgNode)

			if dependency.State != pkggraph.StateUnresolved && dependency.State != pkggraph.StateBuild {
				return
			}

			dependencySRPM := filepath.Base(dependency.SrpmPath)
			if pkgSRPM == dependencySRPM {
				return
			}

			dependencyName := nodeDependencyName(dependency)
			insertIfMissing(srpmsBlockedBy, pkgSRPM, dependencyName)

			return
		})

	}

	printTitle("[INDIRECT] SRPMs closest to being ready to build")
	printReversedMap(srpmsBlockedBy, "total unmet dependencies", maxResults)
}

// nodeDependencyName returns a common dependency name for a node that will be shared across similair Meta/Run/Build nodes for the same package.
func nodeDependencyName(node *pkggraph.PkgNode) (name string) {
	// Prefer the SRPM name if possible, otherwise use the unversioned package name
	srpmName := filepath.Base(node.SrpmPath)
	if srpmName == "" || srpmName == "<NO_SRPM_PATH>" {
		name = node.VersionedPkg.Name
	} else {
		name = srpmName
	}

	return
}

// printTitle prints a formatted title
func printTitle(title string) {
	logger.Log.Info("")
	logger.Log.Info("================================================")
	logger.Log.Info(title)
	logger.Log.Info("================================================")
}

// sortMap returns a sorted slice of a map. If inverse is set, it will return the smallest entries first.
// It will sort entries by the number of values each key has. For keys with the same number of entries, it will
// sort alphabetically.
func sortMap(mapToSort map[string][]string, inverse bool) (pairList []mapPair) {
	pairList = make([]mapPair, 0, len(mapToSort))
	for key, value := range mapToSort {
		pairList = append(pairList, mapPair{key, value})
	}

	sort.Slice(pairList, func(i, j int) bool {
		if len(pairList[i].value) == len(pairList[j].value) {
			return pairList[i].key < pairList[j].key
		}

		if inverse {
			return len(pairList[i].value) < len(pairList[j].value)
		}

		return len(pairList[i].value) > len(pairList[j].value)
	})

	return
}

// insertIfMissing appens a value to the key in a map if it is not present.
// Will alter data.
func insertIfMissing(data map[string][]string, key string, value string) {
	if sliceutils.Find(data[key], value) == -1 {
		data[key] = append(data[key], value)
	}
}

// printMap will sort and print the smallest entries, using the valueDescription in the format.
func printReversedMap(data map[string][]string, valueDescription string, maxResults int) {
	const inverse = true
	pairList := sortMap(data, inverse)
	printSlice(pairList, valueDescription, maxResults)
}

// printMap will sort and print the largest entries, using the valueDescription in the format.
func printMap(data map[string][]string, valueDescription string, maxResults int) {
	const inverse = false
	pairList := sortMap(data, false)
	printSlice(pairList, valueDescription, maxResults)
}

// printSlice prints the first maxResults entries, using the valueDescription in the format.
func printSlice(pairList []mapPair, valueDescription string, maxResults int) {
	if len(pairList) == 0 {
		return
	}

	for i, pair := range pairList {
		if i >= maxResults {
			break
		}
		logger.Log.Infof("%d: %s - %d %s", i+1, pair.key, len(pair.value), valueDescription)
		for _, value := range pair.value {
			logger.Log.Debugf("--> %s", value)
		}
	}
}
