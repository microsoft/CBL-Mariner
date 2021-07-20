# CBL-Mariner Changelog

All notable changes to this project will be documented in this file. For each notable change , please create an entry under the "Unreleased" header in a relevant category with a link to the related PR. If there is no relevant category present, please add one as appropriate.

Suggested categories: "Security Fixes", "Package Additions", "Package Version Updates", "Package Test Fixes", "Toolkit Changes".

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

### [Unreleased]

#### Security Fixes

- CVE-2021-20208 in `cifs-utils` ([#910](https://github.com/microsoft/CBL-Mariner/pull/917))
- CVE-2021-28965 in `ruby` ([#911](https://github.com/microsoft/CBL-Mariner/pull/911))
- CVE-2021-27419 in `uclibc` ([#917](https://github.com/microsoft/CBL-Mariner/pull/917))

#### Package Additions

- `python3-Cython` ([#924](https://github.com/microsoft/CBL-Mariner/pull/924))

#### Package Version Updates

- `go`: 1.15.7 -> 1.15.11 ([#890](https://github.com/microsoft/CBL-Mariner/pull/890))
- `device-mapper-multipath`: 0.8.4 -> 0.8.6
- `kernel`, `kernel-headers`, `kernel-hyperv`, `hyperv-daemon` packages: 50.10.28.1 -> 5.10.32.1 ([#913](https://github.com/microsoft/CBL-Mariner/pull/913))
- `uclibc-ng`: 1.0.36 -> 1.0.37 ([#917](https://github.com/microsoft/CBL-Mariner/pull/917))
- `maven`: 3.6.3 -> 3.8.1 ([#920](https://github.com/microsoft/CBL-Mariner/pull/920))
- `kubernetes`: 1.18.17-hotfix.20210428 -> 1.18.17-hotfix.20210505 ([#925](https://github.com/microsoft/CBL-Mariner/pull/925))
- `kubernetes`: 1.19.9-hotfix.20210428 -> 1.19.9-hotfix.20210505 ([#925](https://github.com/microsoft/CBL-Mariner/pull/925))
- `kubernetes`: 1.20.5-hotfix.20210428 -> 1.20.5-hotfix.20210505 ([#925](https://github.com/microsoft/CBL-Mariner/pull/925))
- `dotnet-runtime`, `aspnetcore-runtime`: 3.1.5 -> 3.1.14 ([#926](https://github.com/microsoft/CBL-Mariner/pull/926))
- `dotnet-sdk`: 3.1.105 -> 3.1.114 ([#926](https://github.com/microsoft/CBL-Mariner/pull/913))

#### Package Test Fixes

- Disable faulty test in `libserf` due to hobbled OpenSSL version ([#916](https://github.com/microsoft/CBL-Mariner/pull/916))

#### Toolkit Changes

- Added heartbeat log for long-running package builds ([#915](https://github.com/microsoft/CBL-Mariner/pull/915))
- Added Secure Boot instructions for HyperV ([#921](https://github.com/microsoft/CBL-Mariner/pull/921))

### [April Update] (1.0.20210430)

TODO: This release and previous releases to be backfilled from release notes.

[Unreleased]: https://github.com/microsoft/CBL-Mariner/compare/1.0-stable..1.0-dev
[April Update]: https://github.com/microsoft/CBL-Mariner/releases/tag/1.0.20210430-1.0
