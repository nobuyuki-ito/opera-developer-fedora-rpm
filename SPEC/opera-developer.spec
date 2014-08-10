%define deb_opera %{name}_%{version}_amd64.deb
%define deb_openssl libssl1.0.0_1.0.1f-1ubuntu2.5_amd64.deb

# these Requires are provided internally because of our bundling or symlinking
%global _excl lib(ssl|crypto|udev)\\.so
%global __requires_exclude %{_excl}
# they're provided internally, but not for other packages please
%global __provides_exclude_from ^.*/%{_excl}.*$

Summary: Opera Developer
Name: opera-developer
Version: 25.0.1583.1
Release: 1%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://get.geo.opera.com/pub/opera-developer/
Source0: http://get.geo.opera.com/pub/opera-developer/%{version}/linux/%{deb_opera}
# download ubuntu package from http://packages.ubuntu.com/trusty-updates/libssl1.0.0
Source1: http://mirrors.kernel.org/ubuntu/pool/main/o/openssl/%{deb_openssl}
Vendor: Opera Software ASA
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: x86_64
Requires: %{_libdir}/libudev.so.1
Requires: systemd-libs

%description
Opera Developer

%prep

%setup -T -n %{name} -c

%build
# nothing to do

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

# provide openssl-1.0.0
ar p %{SOURCE1} data.tar.xz | xz -d | tar x -C $RPM_BUILD_DIR

# extract data from the deb package
ar p %{SOURCE0} data.tar.xz | xz -d | tar x -C $RPM_BUILD_ROOT

# rename libdir
mv $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu/%{name} $RPM_BUILD_ROOT/usr/lib/
rm -rf $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}

# create new symlink
rm -f $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -sr $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

# delete some directories that is not needed on Fedora
rm -rf $RPM_BUILD_ROOT%{_datadir}/{lintian,menu}

# correct opera_sandbox permission
# FATAL:setuid_sandbox_client.cc(283)] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /usr/lib64/opera-developer/opera_sandbox is owned by root and has mode 4755.
chmod 4755 $RPM_BUILD_ROOT%{_libdir}/%{name}/opera_sandbox

# install libssl/libcrypto library
[ ! -d $RPM_BUILD_ROOT%{_libdir}/%{name}/lib ] && mkdir $RPM_BUILD_ROOT%{_libdir}/%{name}/lib
for i in libcrypto libssl; do
	cp -p $RPM_BUILD_DIR/lib/x86_64-linux-gnu/$i.so.* $RPM_BUILD_ROOT%{_libdir}/%{name}/lib
done

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
# create symlink for libudev.so.0
ln -fs %{_libdir}/libudev.so.1 %{_libdir}/%{name}/lib/libudev.so.0

%postun
[ -L %{_libdir}/%{name}/lib/libudev.so.0 ] && rm -f %{_libdir}/%{name}/lib/libudev.so.0

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}

%changelog
* Mon Aug 11 2014 Moritz Barsnick <moritz+rpm@barsnick.net> 25.0.1583.1-1
- update to 25.0.1583.1
- fix symlink to binary
- use latest openssl package from Ubuntu
- use %%{SOURCE} macros
- unpack openssl in %%install phase
- drop xz compression flag for decompression
- drop Packager tag (should be provided by rpmbuild tool chain) and BRs
  (they're all pre-provided on Fedora)
- fix Requires and Provides, in order to not require --no-deps and to not
  provide bogus stuff

* Mon Jun 30 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1543.0
- version up
- change libssl/libcrypto install dir
- add package requires

* Thu Jun 26 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1537.0
- initial build
