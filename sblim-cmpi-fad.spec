#
# Conditional build:
%bcond_with	build	# actually build package (see description)

Summary:	SBLIM CMPI Files And Directories sample provider
Summary(pl.UTF-8):	Przykładowy dostawca danych "Files And Directories" dla SBLIM CMPI
Name:		sblim-cmpi-fad
Version:	0.5.0
Release:	0.1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	db9b8318005f19df743fefc695a4e507
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-devel
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sample SBLIM CMPI Provider - Files And Directories.

This package doesn't serve any particular purpose other than as
reference and template for CMPI provider packages. It allows to access
files and directories beneath /usr/include on the local file system of
the CIM server.

%description -l pl.UTF-8
Przykładowy dostawca danych SBLIM CMPI - Files And Directories (pliki
i katalogi).

Ten pakiet nie służy do żadnego konkretnego celu, innego niż przykład
i szablon dla innych pakietów dostawców CMPI. Umożliwia dostęp do
plików i katalogów poniżej /usr/include w lokalnym systemie plików
serwera CIM.

%prep
%setup -q

%if %{without build}
echo "This is sample/reference package, not meant to be distributed in binary form"
exit 1
%endif

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.{la,so}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/CWS_FAD.registration \
	-m %{_datadir}/%{name}/CWS_FAD.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/CWS_FAD.registration \
		-m %{_datadir}/%{name}/CWS_FAD.mof >/dev/null
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libCWS_FileUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCWS_FileUtils.so.0
%attr(755,root,root) %{_libdir}/libcwsutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcwsutil.so.0
%attr(755,root,root) %{_libdir}/cmpi/libCWS_Directory.so*
%attr(755,root,root) %{_libdir}/cmpi/libCWS_DirectoryContainsFile.so*
%attr(755,root,root) %{_libdir}/cmpi/libCWS_PlainFile.so*
%dir %{_datadir}/sblim-cmpi-fad
%{_datadir}/sblim-cmpi-fad/CWS_FAD.mof
%{_datadir}/sblim-cmpi-fad/CWS_FAD.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-fad/provider-register.sh
