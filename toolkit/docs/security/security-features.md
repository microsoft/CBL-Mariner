# CBL-Mariner operating system security features

| **Type**              | **Feature**                           | **Status** |**Additional information** |
|-----------------------|---------------------------------------|------------|---------------------------|
| **Networking**        |                                       |            |
|                       | Configurable Firewall                 | By default | [iptables](https://git.netfilter.org/)
|                       | SYN cookies                           | By default | [CONFIG_SYN_COOKIES=y](https://github.com/torvalds/linux/blob/master/net/ipv4/Kconfig)
|                       |                                       |            |
| **Updates**           |                                       |            |
|                       | Signed updates                        | By default | [tdnf](https://github.com/vmware/tdnf), [dnf](https://github.com/rpm-software-management/dnf)
|                       |                                       |            |
| **Build options**     |                                       |            |
|                       | Built as PIE                          | By default | [-fPIE, -pie](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html#index-fpie)
|                       | Built with Stack Protector Strong     | By default | [-fstack-protector](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html#index-fstack-protector), [-fstack-protector-strong](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html#index-fstack-protector-strong)
|                       | Built with Format Security            | By default | [-Wformat-security](https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Warning-Options.html)
|                       | Built with Fortify Source             | By default | [\_FORTIFY_SOURCE](https://www.gnu.org/software/libc/manual/html_node/Feature-Test-Macros.html)
|                       | Built with \--enable-bind-now         | By default | [--enable-bind-now](https://www.gnu.org/software/libc/manual/html_node/Configuring-and-compiling.html)
|                       | Built with RELRO                      | By default | [relro](https://sourceware.org/binutils/docs/ld/Options.html)
|                       |                                       |            |
| **Address Space Layout <br/>Randomization (ASLR)**|           |            |
|                       | Stack ASLR                            | By default | Available in the mainline kernel since 2.6.15
|                       | Libs/mmap ASLR                        | By default | Available in the mainline kernel since 2.6.15
|                       | Exec ASLR                             | By default | Available in the mainline kernel since 2.6.25
|                       | brk ASLR                              | By default | Available in the mainline kernel since 2.6.22
|                       | VDSO ASLR                             | By default | Available for x86_64 in the mainline kernel since 2.6.22
|                       |                                       |            |
| **Kernel hardening**  |                                       |            |
|                       | /proc/\$pid/maps protection           | By default | Enabled by default since mainline kernel 2.6.27
|                       | Symlink restrictions                  | By default | [fs.protected_symlinks](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html?highlight=protected_symlinks)
|                       | Hardlink restrictions                 | By default | [fs.protected_hardlinks](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html?highlight=protected_hardlinks)
|                       | 0-address protection                  | By default | [vm.mmap_min_addr](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html?highlight=mmap_min_addr)
|                       | Kernel Address Display Restriction    | By default | [kernel.kptr_restrict](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html?highlight=kptr_restrict)
|                       | Block module loading                  | Available  | [kernel.modules_disabled](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html?highlight=modules_disabled#modules-disabled)
|                       | /dev/mem protection                   | By default | [CONFIG_STRICT_DEVMEM=y](https://github.com/torvalds/linux/blob/master/lib/Kconfig.debug)
|                       | /dev/kmem disabled                    | By default | [CONFIG_DEVKMEM=n](https://github.com/torvalds/linux/blob/master/drivers/char/Kconfig)
|                       | Kernel Module RO/NX                   | By default | [CONFIG_STRICT_MODULE_RWX=y](https://github.com/torvalds/linux/blob/master/arch/Kconfig)
|                       | Write-protect kernel .rodata sections | By default | [CONFIG_STRICT_KERNEL_RWX=y](https://github.com/torvalds/linux/blob/master/arch/Kconfig)
|                       | Kernel Stack Protector                | By default | [CONFIG_STACKPROTECTOR=y](https://github.com/torvalds/linux/blob/master/arch/Kconfig)
|                       |                                       |            |
|**gcc/glibc hardening**|                                       |            |
|                       | Overflow checking in new operator     | By default | [gcc](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19351)
|                       | Pointer Obfuscation                   | By default | [glibc pointer encryption](https://sourceware.org/glibc/wiki/PointerEncryption)
|                       | Heap Consistency Checking             | By default | [glibc Heap Consistency Checking](https://www.gnu.org/software/libc/manual/html_node/Heap-Consistency-Checking.html)
|                       |                                       |            |
|**System call filtering**|                                     |            |
|                       | Syscall Filtering (seccomp)           | Available  | [CONFIG_SECCOMP_FILTER=y](https://github.com/torvalds/linux/blob/master/arch/Kconfig)
|                       | Seccomp sandbox                       | Available  | [PR_SET_SECCOMP](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html?highlight=pr_set_seccomp)
|                       |                                       |            |
| **Process isolation** |                                       |            |
|                       | Ptrace Mitigation                     | Available  | [Yama](https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html)
|                       | User namespaces                       | Available  | [CONFIG_USER_NS=y](https://github.com/torvalds/linux/blob/master/init/Kconfig)
|                       | Private /tmp for systemd services     | Available  | [PrivateTmp](https://systemd.io/TEMPORARY_DIRECTORIES/)
|                       | Polyinstantiate /tmp, /var/tmp,<br/>and user home folders | Available | [namespace.conf](http://www.linux-pam.org/Linux-PAM-html/sag-pam_namespace.html)
|                       |                                       |            |
| **Encrypted Storage** |                                       |            |
|                       | Encrypted Volumes                     | Available  | Encrypt during OS installation
|                       |                                       |            |
| **Miscellaneous**     |                                       |            |
|                       | Password hashing                      | By default | SHA-512
|                       | Filesystem Capabilities               | Available  | [Capabilities](https://github.com/torvalds/linux/blob/master/Documentation/security/credentials.rst) and [chattr](https://sourceforge.net/p/e2fsprogs/code/ci/master/tree/misc/chattr.c)
|                       | Tamper Resistant Logs                 | Available  | [journalctl --verify](https://www.freedesktop.org/software/systemd/man/journalctl.html)
|                       | Kernel Lockdown                       | Integrity mode by default | [kernel lockdown](https://github.com/torvalds/linux/blob/master/security/lockdown/Kconfig)


# References
[Fedora Project Security Features Matrix](https://fedoraproject.org/wiki/Security_Features_Matrix)

[Ubuntu Security Features](https://wiki.ubuntu.com/Security/Features)
