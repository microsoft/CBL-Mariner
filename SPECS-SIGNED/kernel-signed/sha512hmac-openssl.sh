#!/bin/bash

# Mocks sha512hmac using the openssl tool.
# Only for use during RPM build.

openssl sha512 -hmac FIPS-FTW-RHT2009 -hex "$1" | cut -f 2 -d ' ' | echo "$(cat -)  $1"