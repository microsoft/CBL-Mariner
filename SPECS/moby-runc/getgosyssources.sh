#!/bin/sh
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# This script generates the sources moby-runc dependent packages.

# golang sys sources are git cloned to latest commit.
GOLANG_SYS=https://github.com/golang/sys.git
GOLANG_SYS_COMMIT=b0526f3d87448f0401ea3f7f3a81aa9e6ab4804d

mkdir -p /build/work/sys-master
cd /build/work/sys-master
git clone ${GOLANG_SYS} .
git fetch --tags origin ${GOLANG_SYS_COMMIT}
git checkout ${GOLANG_SYS_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-sys-${GOLANG_SYS_COMMIT}.tar.gz sys-master
rm -rf /build/work

# golang crypto sources are git cloned to latest commit.
GOLANG_CRYPO=https://github.com/golang/crypto.git
GOLANG_CRYPTO_COMMIT=c07d793c2f9aacf728fe68cbd7acd73adbd04159

mkdir -p /build/work/crypto-master
cd /build/work/crypto-master
git clone ${GOLANG_CRYPO} .
git fetch --tags origin ${GOLANG_CRYPTO_COMMIT}
git checkout ${GOLANG_CRYPTO_COMMIT}
cd /build/
tar -C /build/work -czf ./golang-crypto-${GOLANG_CRYPTO_COMMIT}.tar.gz crypto-master
rm -rf /build/work
