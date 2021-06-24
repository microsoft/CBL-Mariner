#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources for moby-buildx package.
# Git clone is a standard practice of producing source files for moby-* packages.

RUNC_REPO=https://github.com/opencontainers/runc.git
RUNC_COMMIT=b9ee9c6314599f1b4a7f497e1f1f856fe433d3b7
VERSION=v1.0.0-rc95

mkdir -p /build/runc-src
cd /build/runc-src
git clone ${RUNC_REPO}
cd runc
git fetch --tags origin ${RUNC_COMMIT}
git checkout ${RUNC_COMMIT}
cd /build/
tar -C /build/runc-src -czf ./runc-${VERSION}.tar.gz .
rm -rf /build/runc-src

echo "sources generated successfully @ /build/runc-${VERSION}.tar.gz"
