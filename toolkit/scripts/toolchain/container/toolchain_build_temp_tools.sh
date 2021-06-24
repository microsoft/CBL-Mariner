#!/bin/sh
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
set -x
if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS
cd $LFS/sources

touch $LFS/logs/temptoolchain/status_temp_toolchain_build_started

cat /home/lfs/.bashrc
LFS_TGT=$(uname -m)-lfs-linux-gnu

echo Binutils-2.36.1 - Pass 1
tar xf binutils-2.36.1.tar.xz
pushd binutils-2.36.1
mkdir -v build
cd build
../configure --prefix=/tools \
    --with-sysroot=$LFS \
    --with-lib-path=/tools/lib \
    --target=$LFS_TGT \
    --disable-nls \
    --disable-werror
make -j$(nproc)
mkdir -v /tools/lib && ln -sv lib /tools/lib64
make install
popd
rm -rf binutils-2.36.1

touch $LFS/logs/temptoolchain/status_binutils_pass1_complete

echo GCC-9.1.0 - Pass 1
tar xf gcc-9.1.0.tar.xz
pushd gcc-9.1.0
tar xf ../mpfr-4.0.1.tar.xz
mv -v mpfr-4.0.1 mpfr
tar xf ../gmp-6.1.2.tar.xz
mv -v gmp-6.1.2 gmp
tar xf ../mpc-1.1.0.tar.gz
mv -v mpc-1.1.0 mpc
case $(uname -m) in
    x86_64)
      for file in gcc/config/{linux,i386/linux{,64}}.h
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
    aarch64)
      for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h -o -name linux-eabi.h -o -name linux-elf.h -o -name aarch64-linux.h)
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
esac
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
mkdir -v build
cd       build
../configure                                       \
    --target=$LFS_TGT                              \
    --prefix=/tools                                \
    --with-glibc-version=2.11                      \
    --with-sysroot=$LFS                            \
    --with-newlib                                  \
    --without-headers                              \
    --with-local-prefix=/tools                     \
    --with-native-system-header-dir=/tools/include \
    --disable-nls                                  \
    --disable-shared                               \
    --disable-multilib                             \
    --disable-decimal-float                        \
    --disable-threads                              \
    --disable-libatomic                            \
    --disable-libgomp                              \
    --disable-libquadmath                          \
    --disable-libssp                               \
    --disable-libvtv                               \
    --disable-libstdcxx                            \
    --enable-languages=c,c++
make -j$(nproc)
make install
popd
rm -rf gcc-9.1.0

touch $LFS/logs/temptoolchain/status_gcc_pass1_complete

echo Linux-5.10.42.1 API Headers
tar xf kernel-5.10.42.1.tar.gz
pushd CBL-Mariner-Linux-Kernel-rolling-lts-mariner-5.10.42.1
make mrproper
make headers
cp -rv usr/include/* /tools/include
popd
rm -rf CBL-Mariner-Linux-Kernel-rolling-lts-mariner-5.10.42.1

touch $LFS/logs/temptoolchain/status_kernel_headers_complete

echo glibc-2.28
tar xf glibc-2.28.tar.xz
pushd glibc-2.28
mkdir -v build
cd       build
../configure                             \
      --prefix=/tools                    \
      --disable-werror                   \
      --host=$LFS_TGT                    \
      --build=$(../scripts/config.guess) \
      --enable-kernel=3.2                \
      --with-headers=/tools/include      \
      libc_cv_forced_unwind=yes          \
      libc_cv_c_cleanup=yes
# Build with single processor due to LFS warning about glibc errors seen with parallel make
make -j1
make install
echo sanity check - temptoolchain - glibc
set +e
echo 'int main(){}' > dummy.c
$LFS_TGT-gcc dummy.c
readelf -l a.out | grep ': /tools'
case $(uname -m) in
  x86_64)
    echo Expected: '[Requesting program interpreter: /tools/lib64/ld-linux-x86-64.so.2]'
  ;;
  aarch64)
    echo Expected: '[Requesting program interpreter: /tools/lib/ld-linux-aarch64.so.1]'
  ;;
esac
rm -v dummy.c a.out
set -e
echo End sanity check - temptoolchain - glibc
popd
rm -rf glibc-2.28

touch $LFS/logs/temptoolchain/status_glibc_complete

echo Libstdc++ from GCC-9.1.0
tar xf gcc-9.1.0.tar.xz
pushd gcc-9.1.0
mkdir -v build
cd       build
../libstdc++-v3/configure           \
    --host=$LFS_TGT                 \
    --prefix=/tools                 \
    --disable-multilib              \
    --disable-nls                   \
    --disable-libstdcxx-threads     \
    --disable-libstdcxx-pch         \
    --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/9.1.0
make -j$(nproc)
make install
popd
rm -rf gcc-9.1.0

touch $LFS/logs/temptoolchain/status_libstdc++_complete

echo Binutils-2.36.1 - Pass 2
tar xf binutils-2.36.1.tar.xz
pushd binutils-2.36.1
mkdir -v build
cd build
CC=$LFS_TGT-gcc                  \
AR=$LFS_TGT-ar                   \
RANLIB=$LFS_TGT-ranlib           \
../configure                   	 \
	    --prefix=/tools            \
	    --disable-nls              \
	    --disable-werror           \
	    --with-lib-path=/tools/lib \
	    --with-sysroot
make -j$(nproc)
make install
make -C ld clean
make -C ld LIB_PATH=/usr/lib:/lib
cp -v ld/ld-new /tools/bin
popd
rm -rf binutils-2.36.1

touch $LFS/logs/temptoolchain/status_binutils_pass2_complete

echo GCC-9.1.0 - Pass 2
tar xf gcc-9.1.0.tar.xz
pushd gcc-9.1.0
cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
  `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h
case $(uname -m) in
    x86_64)
      for file in gcc/config/{linux,i386/linux{,64}}.h
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
    aarch64)
      for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h -o -name linux-eabi.h -o -name linux-elf.h -o -name aarch64-linux.h)
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
esac
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
tar -xf ../mpfr-4.0.1.tar.xz
mv -v mpfr-4.0.1 mpfr
tar -xf ../gmp-6.1.2.tar.xz
mv -v gmp-6.1.2 gmp
tar -xf ../mpc-1.1.0.tar.gz
mv -v mpc-1.1.0 mpc
mkdir -v build
cd       build
CC=$LFS_TGT-gcc                                    \
CXX=$LFS_TGT-g++                                   \
AR=$LFS_TGT-ar                                     \
RANLIB=$LFS_TGT-ranlib                             \
../configure                                       \
    --prefix=/tools                                \
    --with-local-prefix=/tools                     \
    --with-native-system-header-dir=/tools/include \
    --enable-languages=c,c++                       \
    --disable-libstdcxx-pch                        \
    --disable-multilib                             \
    --disable-bootstrap                            \
    --disable-libgomp
make -j$(nproc)
make install
ln -sv gcc /tools/bin/cc
# Sanity check
set +e
echo sanity check - temptoolchain - gcc 9.1.0 pass2
echo 'int main(){}' > dummy.c
cc dummy.c
readelf -l a.out | grep ': /tools'
case $(uname -m) in
  x86_64)
    echo Expected: '[Requesting program interpreter: /tools/lib64/ld-linux-x86-64.so.2]'
  ;;
  aarch64)
    echo Expected: '[Requesting program interpreter: /tools/lib/ld-linux-aarch64.so.1]'
  ;;
esac
rm -v dummy.c a.out
set -e
echo End sanity check - temptoolchain - gcc 9.1.0 pass2
popd
rm -rf gcc-9.1.0

touch $LFS/logs/temptoolchain/status_gcc_pass2_complete

echo Tcl-8.6.9
tar xf tcl8.6.9-src.tar.gz
pushd tcl8.6.9
cd unix
./configure --prefix=/tools
make -j$(nproc)
make install
chmod -v u+w /tools/lib/libtcl8.6.so
make install-private-headers
ln -sv tclsh8.6 /tools/bin/tclsh
popd
rm -rf tcl8.6.9

touch $LFS/logs/temptoolchain/status_tcl_complete

echo Expect-5.45.4
tar -zxf expect5.45.4.tar.gz
pushd expect5.45.4
cp -v configure{,.orig}
sed 's:/usr/local/bin:/bin:' configure.orig > configure
case $(uname -m) in
    x86_64)
      ./configure --prefix=/tools \
        --with-tcl=/tools/lib \
        --with-tclinclude=/tools/include
    ;;
    aarch64)
      ./configure --prefix=/tools \
        --with-tcl=/tools/lib \
        --with-tclinclude=/tools/include \
        --build=aarch64-unknown-linux-gnu
    ;;
esac
make -j$(nproc)
make SCRIPTS="" install
popd
rm -rf expect5.45.4
touch $LFS/logs/temptoolchain/status_expect_complete

echo DejaGNU-1.6.2
tar xf dejagnu-1.6.2.tar.gz
pushd dejagnu-1.6.2
./configure --prefix=/tools
make install
popd
rm -rf dejagnu-1.6.2

touch $LFS/logs/temptoolchain/status_dejagnu_complete

echo M4-1.4.18
tar xf m4-1.4.18.tar.xz
pushd m4-1.4.18
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf m4-1.4.18

touch $LFS/logs/temptoolchain/status_m4_complete

echo Ncurses-6.2
tar xf ncurses-6.2.tar.gz
pushd ncurses-6.2
sed -i s/mawk// configure
./configure --prefix=/tools \
            --with-shared   \
            --without-debug \
            --without-ada   \
            --enable-widec  \
            --enable-overwrite
make -j$(nproc)
make install
ln -s libncursesw.so /tools/lib/libncurses.so
popd
rm -rf ncurses-6.2

touch $LFS/logs/temptoolchain/status_ncurses_complete

echo Bash-4.4.18
tar xf bash-4.4.18.tar.gz
pushd bash-4.4.18
./configure --prefix=/tools --without-bash-malloc
make -j$(nproc)
make install
ln -sv bash /tools/bin/sh
popd
rm -rf bash-4.4.18

touch $LFS/logs/temptoolchain/status_bash_complete

echo Bison-3.1
tar xf bison-3.1.tar.xz
pushd bison-3.1
./configure --prefix=/tools
# Build with single processor due to errors seen with parallel make
#     cannot stat 'examples/c/reccalc/scan.stamp.tmp': No such file or directory
make -j1
make install
popd
rm -rf bison-3.1

touch $LFS/logs/temptoolchain/status_bison_complete

echo Bzip2-1.0.6
tar xf bzip2-1.0.6.tar.gz
pushd bzip2-1.0.6
make -j$(nproc)
make PREFIX=/tools install
popd
rm -rf bzip2-1.0.6

touch $LFS/logs/temptoolchain/status_bzip2_complete

echo Coreutils-8.30
tar xf coreutils-8.30.tar.xz
pushd coreutils-8.30
./configure --prefix=/tools --enable-install-program=hostname
make -j$(nproc)
make install
popd
rm -rf coreutils-8.30

touch $LFS/logs/temptoolchain/status_coreutils_complete

echo Diffutils-3.6
tar xf diffutils-3.6.tar.xz
pushd diffutils-3.6
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf diffutils-3.6

touch $LFS/logs/temptoolchain/status_diffutils_complete

echo File-5.34
tar xf file-5.34.tar.gz
pushd file-5.34
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf file-5.34

touch $LFS/logs/temptoolchain/status_file_complete

echo Findutils-4.6.0
tar xf findutils-4.6.0.tar.gz
pushd findutils-4.6.0
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' gl/lib/*.c
sed -i '/unistd/a #include <sys/sysmacros.h>' gl/lib/mountlist.c
echo "#define _IO_IN_BACKUP 0x100" >> gl/lib/stdio-impl.h
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf findutils-4.6.0

touch $LFS/logs/temptoolchain/status_findutils_complete

echo Gawk-4.2.1
tar xf gawk-4.2.1.tar.xz
pushd gawk-4.2.1
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf gawk-4.2.1

touch $LFS/logs/temptoolchain/status_gawk_complete

echo Gettext-0.19.8.1
tar xf gettext-0.19.8.1.tar.xz
pushd gettext-0.19.8.1
./configure --disable-shared
make -j$(nproc)
cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /tools/bin
popd
rm -rf gettext-0.19.8.1

touch $LFS/logs/temptoolchain/status_gettext_complete

echo Grep-3.1
tar xf grep-3.1.tar.xz
pushd grep-3.1
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf grep-3.1

touch $LFS/logs/temptoolchain/status_grep_complete

echo Gzip-1.9
tar xf gzip-1.9.tar.xz
pushd gzip-1.9
./configure --prefix=/tools
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
make -j$(nproc)
make install
popd
rm -rf gzip-1.9

touch $LFS/logs/temptoolchain/status_gzip_complete

echo Make-4.2.1
tar xf make-4.2.1.tar.gz
pushd make-4.2.1
sed -i '211,217 d; 219,229 d; 232 d' glob/glob.c
./configure --prefix=/tools --without-guile
make -j$(nproc)
make install
popd
rm -rf make-4.2.1

touch $LFS/logs/temptoolchain/status_make_complete

echo Patch-2.7.6
tar xf patch-2.7.6.tar.xz
pushd patch-2.7.6
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf patch-2.7.6

touch $LFS/logs/temptoolchain/status_patch_complete

echo Perl-5.30.3
tar xf perl-5.30.3.tar.gz
pushd perl-5.30.3
sh Configure -des -Dprefix=/tools -Dlibs=-lm -Uloclibpth -Ulocincpth
make -j$(nproc)
cp -v perl cpan/podlators/scripts/pod2man /tools/bin
mkdir -pv /tools/lib/perl5/5.30.3
cp -Rv lib/* /tools/lib/perl5/5.30.3
popd
rm -rf perl-5.30.3

touch $LFS/logs/temptoolchain/status_perl_complete

echo Python-3.7.4
tar xf Python-3.7.4.tar.xz
pushd Python-3.7.4
sed -i '/def add_multiarch_paths/a \        return' setup.py
./configure --prefix=/tools --without-ensurepip
make -j$(nproc)
make install
popd
rm -rf Python-3.7.4

touch $LFS/logs/temptoolchain/status_python_complete

echo Sed-4.5
tar xf sed-4.5.tar.xz
pushd sed-4.5
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf sed-4.5

touch $LFS/logs/temptoolchain/status_sed_complete

echo Tar-1.30
tar xf tar-1.30.tar.xz
pushd tar-1.30
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf tar-1.30

touch $LFS/logs/temptoolchain/status_tar_complete

echo Texinfo-6.5
tar xf texinfo-6.5.tar.xz
pushd texinfo-6.5
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf texinfo-6.5

touch $LFS/logs/temptoolchain/status_texinfo_complete

echo Xz-5.2.4
tar xf xz-5.2.4.tar.xz
pushd xz-5.2.4
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf xz-5.2.4

touch $LFS/logs/temptoolchain/status_xz_complete

echo zstd-1.4.4
tar xf zstd-1.4.4.tar.gz
pushd zstd-1.4.4
make -j$(nproc)
make install prefix=/tools pkgconfigdir=/tools/lib/pkgconfig
popd
rm -rf zstd-1.4.4

touch $LFS/logs/temptoolchain/status_zstd_complete

touch $LFS/logs/temptoolchain/temp_toolchain_complete

echo Done with script
