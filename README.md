# CBL-Mariner

| Release Branch | Status                                                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0            | [![1.0 Status](https://github.com/microsoft/CBL-Mariner/workflows/Verify%20Quickstart%201.0/badge.svg)](https://github.com/microsoft/CBL-Mariner/actions?query=workflow%3A%22Verify+Quickstart+1.0%22) |

CBL-Mariner is an internal Linux distribution for Microsoft’s cloud infrastructure and edge products and services. CBL-Mariner is designed to provide a consistent platform for these devices and services and will enhance Microsoft’s ability to stay current on Linux updates. This initiative is part of Microsoft’s increasing investment in a wide range of Linux technologies, such as [SONiC](https://azure.microsoft.com/en-us/blog/sonic-the-networking-switch-software-that-powers-the-microsoft-global-cloud/), [Azure Sphere OS](https://docs.microsoft.com/en-us/azure-sphere/product-overview/what-is-azure-sphere) and [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/about). CBL-Mariner is being shared publicly as part of Microsoft’s commitment to Open Source and to contribute back to the Linux community. CBL-Mariner does not change our approach or commitment to any existing third-party Linux distribution offerings. 

CBL-Mariner has been engineered with the notion that a small common core set of packages can address the universal needs of first party cloud and edge services while allowing individual teams to layer additional packages on top of the common core to produce images for their workloads. This is made possible by a simple build system that enables:

- **Package Generation:** This produces the desired set of RPM packages from SPEC files and source files. 
- **Image Generation:** This produces the desired image artifacts like ISOs or VHDs from a given set of packages. 

Whether deployed as a container or a container host, CBL-Mariner consumes limited disk and memory resources. The lightweight characteristics of CBL-Mariner also provides faster boot times and a minimal attack surface. By focusing the features in the core image to just what is needed for our internal cloud customers there are fewer services to load, and fewer attack vectors. 

When security vulnerabilities arise, CBL-Mariner supports both a package-based update model and an image based update model.  Leveraging the common [RPM Package Manager](https://rpm.org/) system, CBL-Mariner makes the latest security patches and fixes available for download with the goal of fast turn-around times.   

# Getting Started with CBL-Mariner: 

Instructions for building CBL-Mariner may be found here: [Toolkit Documentation](./toolkit/README.md)

## ISO
You can try out CBL-Mariner with the following ISO: [x86_64 ISO](https://osrelease.download.prss.microsoft.com/pr/download/Mariner-1.0-x86_64.iso)

### ISO Quickstart with Hyper-V
**Create VHD(X) Virtual Machine with Hyper-V**

1. From Hyper-V Select _Action->New->Virtual Machine_.
1. Provide a name for your VM and press _Next >_.
1. Select _Generation 1_ (VHD) or _Generation 2_ (VHDX), then press _Next >_.
1. Change Memory size if desired, then press _Next >_.
1. Select a virtual switch, then press _Next >_.
1. Select _Create a virtual hard disk_, choose a location for your VHD(X) and set your desired disk Size.  Then press _Next >_.
1. Select _Install an operating system from a bootable image file_ and browse to your Demo ISO. 
1. Press _Finish_.

**[Gen2/VHDX Only] Additional Boot Configuration**

1. Right click your virtual machine from Hyper-V Manager
1. Select _Settings..._
1. Select Security and under _Template:_ select _Microsoft UEFI Certificate Authority_.
1. Select Firmware and adjust the boot order so DVD is first and Hard Drive is second.
1. Select _Apply_ to apply all changes.

**Boot ISO**
1. Right click your VM and select _Connect..._.
1. Select _Start_.
1. Follow the installer prompts to install your image
1. When installation completes, select `[Restart]` to reboot the machine. The installation ISO will be automatically ejected.
1. *[Optional]* Shut down VM and adjust boot order to place Hard Drive first. Otherwise if Network boot occurs, your VM will attempt to PXE boot with a timeout of about 2 minutes before trying the next boot option.
1. When prompted sign in to your CBL-Mariner system using the user name and password provisioned through the Installer.

### Verify ISO via Checksum
We also provide the ISO checksum in a file and GPG signature of that file so you can independently verify the contents.

Steps:
1. Install `gpg` onto your system.
   - On Ubuntu, you can run: `sudo apt-get install gpg`
1. Download Mariner RPM key from the GitHub repo: [Mariner RPM key](https://github.com/microsoft/CBL-Mariner/blob/1.0-stable/SPECS/mariner-repos/MICROSOFT-RPM-GPG-KEY)
1. Import the Mariner RPM key into gpg: `gpg --import <path to key>`
1. Download [ISO Checksum](https://osrelease.download.prss.microsoft.com/pr/download/Mariner-1.0-x86_64.iso.sha256) and [ISO Checksum Signature](https://osrelease.download.prss.microsoft.com/pr/download/Mariner-1.0-x86_64.iso.sha256.gpg) files.
1. Verify the checksum file's signature is associated with this checksum file using gpg: `gpg --verify <path to checksum signature file> <path to checksum file>`
   - Sample output:
   ```bash
   $ gpg --verify Mariner-1.0-x86_64.iso.sha256.gpg Mariner-1.0-x86_64.iso.sha256
   gpg: Signature made Sun 20 Jun 2021 12:19:54 AM UTC
   gpg:                using RSA key 0CD9FED33135CE90
   gpg: Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 2BC9 4FFF 7015 A5F2 8F15  37AD 0CD9 FED3 3135 CE90
   ```
   The important part is checking that you have a good signature from the Mariner RPM key imported earlier. Depending on your installed certificates, you might get a warning about the key itself not certified with a trusted signature.
1. Verify that the output of `sha256sum <path to ISO File>` matches the SHA256 checksum found in the checksum file.

# Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

# Acknowledgments 

Any Linux distribution, including CBL-Mariner, benefits from contributions by the open software community. We gratefully acknowledge all contributions made from the broader open source community, in particular:

1) The [Photon OS Project](https://vmware.github.io/photon/) for SPEC files originating from the Photon distribution.   

2) [The Fedora Project](https://start.fedoraproject.org/) for SPEC files, particularly with respect to QT, DNF and several of their dependencies. 

3) [GNU](https://www.gnu.org/) and the [Free Software Foundation](https://www.fsf.org/)

4) [Linux from Scratch](http://www.linuxfromscratch.org)

5) [Openmamba](https://openmamba.org/en/) for SPEC files
