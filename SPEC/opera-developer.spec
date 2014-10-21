%define deb_opera %{name}_%{version}_amd64.deb
%define deb_openssl libssl1.0.0_1.0.1f-1ubuntu2.7_amd64.deb

Summary: Opera Developer
Name: opera-developer
Version: 26.0.1655.0
Release: 1%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://get.geo.opera.com/pub/opera-developer/
Source0: http://get.geo.opera.com/pub/opera-developer/%{version}/linux/%{deb_opera}
# download ubuntu package from http://packages.ubuntu.com/trusty-updates/libssl1.0.0
Source1: http://mirrors.kernel.org/ubuntu/pool/main/o/openssl/%{deb_openssl}
Vendor: Opera Software ASA
Packager: Nobuyuki Ito
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: x86_64
Requires: systemd-libs
BuildRequires: binutils xz tar
Provides: libcrypto.so.1.0.0()(64bit) libudev.so.0()(64bit)

%description
Opera Developer

%prep

%setup -T -n %{name} -c

%build
ar p $RPM_SOURCE_DIR/%{deb_openssl} data.tar.xz | xz -d -9 | tar x -C $RPM_BUILD_DIR

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

# extract data from the deb package
ar p $RPM_SOURCE_DIR/%{deb_opera} data.tar.xz | xz -d -9 | tar x -C $RPM_BUILD_ROOT

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
# create symlink for libudev
[ -e %{_libdir}/libudev.so.1 ] && ln -fs %{_libdir}/libudev.so.1 %{_libdir}/%{name}/lib/libudev.so.0

%postun
[ -L %{_libdir}/%{name}/lib/libudev.so.0 ] && rm -f %{_libdir}/%{name}/lib/libudev.so.0

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}

%changelog
* Wed Oct 22 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1655.0
- version up

* Sat Sep 27 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 26.0.1632.0
- version up
- fix missing library requires
- fix missing symlink to opera-developer

* Sat Aug 30 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 25.0.1597.0
- version up

* Mon Jul 21 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1558.3
- version up

* Mon Jun 30 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1543.0
- version up
- change libssl/libcrypto install dir
- add package requires

* Thu Jun 26 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1537.0
- initial build
