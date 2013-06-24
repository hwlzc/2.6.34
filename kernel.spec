Name: kernel
Summary: The Linux Kernel
Version: 2.6.34
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: http://www.kernel.org
Source: kernel-2.6.34.tar.gz
BuildRoot: /var/tmp/%{name}-%{PACKAGE_VERSION}-root
Provides:  kernel-2.6.34
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%description
The Linux Kernel, the operating system core itself

%prep
%setup -q

%build
make clean && make %{?_smp_mflags}

%install
%ifarch ia64
mkdir -p $RPM_BUILD_ROOT/boot/efi $RPM_BUILD_ROOT/lib/modules
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%else
mkdir -p $RPM_BUILD_ROOT/boot $RPM_BUILD_ROOT/lib/modules
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%endif
INSTALL_MOD_PATH=$RPM_BUILD_ROOT make %{_smp_mflags} KBUILD_SRC= modules_install
%ifarch ia64
cp $KBUILD_IMAGE $RPM_BUILD_ROOT/boot/efi/vmlinuz-2.6.34
ln -s efi/vmlinuz-2.6.34 $RPM_BUILD_ROOT/boot/
%else
%ifarch ppc64
cp vmlinux arch/powerpc/boot
cp arch/powerpc/boot/$KBUILD_IMAGE $RPM_BUILD_ROOT/boot/vmlinuz-2.6.34
%else
cp $KBUILD_IMAGE $RPM_BUILD_ROOT/boot/vmlinuz-2.6.34
%endif
%endif
cp System.map $RPM_BUILD_ROOT/boot/System.map-2.6.34
cp .config $RPM_BUILD_ROOT/boot/config-2.6.34
%ifnarch ppc64
cp vmlinux vmlinux.orig
bzip2 -9 vmlinux
mv vmlinux.bz2 $RPM_BUILD_ROOT/boot/vmlinux-2.6.34.bz2
mv vmlinux.orig vmlinux
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir /lib/modules
/lib/modules/2.6.34
/lib/firmware
/boot/*

