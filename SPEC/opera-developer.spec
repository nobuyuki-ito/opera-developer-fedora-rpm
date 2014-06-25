%define deb_opera %{name}_%{version}_amd64.deb
%define deb_openssl libssl1.0.0_1.0.1f-1ubuntu2.4_amd64.deb

Summary: Opera Developer
Name: opera-developer
Version: 24.0.1537.0
Release: 0%{dist}
License: Proprietary
Group: Applications/Internet
URL: http://get.geo.opera.com/pub/opera-developer/
Source0: http://get.geo.opera.com/pub/opera-developer/%{version}/linux/%{deb_opera}
Source1: http://mirrors.kernel.org/ubuntu/pool/main/o/openssl/%{openssl_deb}
Vendor: Opera Software ASA
Packager: Nobuyuki Ito
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: x86_64
Requires: gtk2
BuildRequires: binutils xz tar

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
mv $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu/%{name} $RPM_BUILD_ROOT/usr/lib/
rm -rf $RPM_BUILD_ROOT/usr/lib/x86_64-linux-gnu
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -sr $RPM_BUILD_ROOT%{_libdir}/%{name}/opera $RPM_BUILD_ROOT%{_bindir}/%{name}
rm -rf $RPM_BUILD_ROOT%{_datadir}/{lintian,menu}
# FATAL:setuid_sandbox_client.cc(283)] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /usr/lib64/opera-developer/opera_sandbox is owned by root and has mode 4755.
chmod 4755 $RPM_BUILD_ROOT%{_libdir}/%{name}/opera_sandbox

# install libssl/libcrypto library
[ ! -d $RPM_BUILD_ROOT/lib64 ] && mkdir $RPM_BUILD_ROOT/lib64
for i in libcrypto libssl; do
	cp -p $RPM_BUILD_DIR/lib/x86_64-linux-gnu/$i.so.1.0.0 $RPM_BUILD_ROOT/lib64
done

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
/lib64/libcrypto.so.*
/lib64/libssl.so.*
%{_libdir}/%{name}
%{_datadir}

%changelog
* Thu Jun 26 2014 Nobuyuki Ito <nobu.1026@gmail.com> - 24.0.1537.0
- initial build
