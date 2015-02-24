#
# Conditional build:
%bcond_without	python		# build without python bindings
#
Summary:	Next Generation of POSIX capabilities library
Summary(pl.UTF-8):	Biblioteka POSIX capabilities nowej generacji
Name:		libcap-ng
Version:	0.7.4
Release:	2
License:	LGPL v2.1+ (library), GPL v2+ (utilities)
Group:		Libraries
Source0:	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
# Source0-md5:	55c57c0673b944ea1a755bcb2636dabd
Patch0:		vserver.patch
URL:		http://people.redhat.com/sgrubb/libcap-ng/
BuildRequires:	attr-devel
BuildRequires:	automake
BuildRequires:	linux-libc-headers >= 7:2.6.33.1
%{?with_python:BuildRequires:	python-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_python:BuildRequires:	swig-python}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libcap-ng library should make programming with POSIX capabilities
easier. The library has some utilities to help you analyse a system
for apps that may have too much privileges.

%description -l pl.UTF-8
Biblioteka libcap-ng powinna uczynić programowanie POSIX-owych
capabilities łatwiejszym. Zawiera narzędzia pomagające w analizie
systemu pod kątem aplikacji posiadających zbyt duże uprawnienia.

%package devel
Summary:	Header files for libcap-ng library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcap-ng
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	linux-libc-headers >= 7:2.6.26

%description devel
Header files for libcap-ng library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcap-ng.

%package static
Summary:	Static libcap-ng library
Summary(pl.UTF-8):	Statyczna biblioteka libcap-ng
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcap-ng library.

%description static -l pl.UTF-8
Statyczna biblioteka libcap-ng.

%package utils
Summary:	Utilities for analysing and setting file capabilities
Summary(pl.UTF-8):	Narzędzia do analizy i ustawiania capabilities dla plików
License:	GPL v2+
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
This package contains applications to analyse the POSIX capabilities
of all the program running on a system. It also lets you set the file
system based capabilities.

%description utils -l pl.UTF-8
Ten pakiet zawiera aplikacje do analizy POSIX-owych capabilities
wszystkich programów działających w systemie; pozwala także ustawiać
capabilities w systemie plików.

%package -n python-capng
Summary:	Python interface to libcap-ng library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki libcap-ng
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-capng
Python interface to libcap-ng library.

%description -n python-capng -l pl.UTF-8
Pythonowy interfejs do biblioteki libcap-ng.

%prep
%setup -q
%patch0 -p1

# force regeneration after captab.h change in vserver patch
%{__rm} bindings/python/capng.py

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libcap-ng.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcap-ng.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libcap-ng.so

%if %{with python}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_capng.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) /%{_lib}/libcap-ng.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libcap-ng.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcap-ng.so
%{_libdir}/libcap-ng.la
%{_includedir}/cap-ng.h
%{_pkgconfigdir}/libcap-ng.pc
%{_aclocaldir}/cap-ng.m4
%{_mandir}/man3/capng_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcap-ng.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/captest
%attr(755,root,root) %{_bindir}/filecap
%attr(755,root,root) %{_bindir}/netcap
%attr(755,root,root) %{_bindir}/pscap
%{_mandir}/man8/captest.8*
%{_mandir}/man8/filecap.8*
%{_mandir}/man8/netcap.8*
%{_mandir}/man8/pscap.8*

%if %{with python}
%files -n python-capng
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_capng.so
%{py_sitedir}/capng.py[co]
%endif
