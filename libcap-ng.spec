#
# Conditional build:
%bcond_without	python3		# CPython 3 bindings
%bcond_without	static_libs	# static libraries
%bcond_with	cap_audit	# cap-audit utility (requires btf capable kernel to build)
#
Summary:	Next Generation of POSIX capabilities library
Summary(pl.UTF-8):	Biblioteka POSIX capabilities nowej generacji
Name:		libcap-ng
Version:	0.9.3
Release:	1
Epoch:		1
License:	LGPL v2.1+ (library), GPL v2+ (utilities)
Group:		Libraries
Source0:	https://github.com/stevegrubb/libcap-ng/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a7667d27aa461f30d118a25cd4a62ede
Patch0:		vserver.patch
URL:		https://people.redhat.com/sgrubb/libcap-ng/
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
BuildRequires:	linux-libc-headers >= 7:2.6.33.1
BuildRequires:	pkgconfig
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python3:BuildRequires:	python3-modules >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.527
%{?with_python3:BuildRequires:	swig-python}
%if %{with cap_audit}
BuildRequires:	audit-libs-devel
BuildRequires:	clang
BuildRequires:	kernel-tools
BuildRequires:	libbpf-devel
# +some data in /sys/kernel/btf/vmlinux ???
%endif
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
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
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
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
Static libcap-ng library.

%description static -l pl.UTF-8
Statyczna biblioteka libcap-ng.

%package utils
Summary:	Utilities for analysing and setting file capabilities
Summary(pl.UTF-8):	Narzędzia do analizy i ustawiania capabilities dla plików
License:	GPL v2+
Group:		Applications/System
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description utils
This package contains applications to analyse the POSIX capabilities
of all the program running on a system. It also lets you set the file
system based capabilities.

%description utils -l pl.UTF-8
Ten pakiet zawiera aplikacje do analizy POSIX-owych capabilities
wszystkich programów działających w systemie; pozwala także ustawiać
capabilities w systemie plików.

%package -n python3-capng
Summary:	Python 3 interface to libcap-ng library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki libcap-ng
Group:		Libraries/Python
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	python-capng < 1:0.8.4

%description -n python3-capng
Python 3 interface to libcap-ng library.

%description -n python3-capng -l pl.UTF-8
Interfejs Pythona 3 do biblioteki libcap-ng.

%prep
%setup -q
%patch -P 0 -p1

# force regeneration after captab.h change in vserver patch
%{__rm} -f bindings/python3/capng.py

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	BPFTOOL=/usr/sbin/bpftool \
	%{?with_cap_audit:--enable-cap-audit} \
	--enable-deprecated \
	%{__enable_disable static_libs static} \
	%{!?with_python3:--without-python3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{%{_lib},%{bash_compdir}}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libcap-ng.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcap-ng.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libcap-ng.so

%{__mv} $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/libcap-ng.bash_completion $RPM_BUILD_ROOT%{bash_compdir}/libcap-ng

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_capng.la
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
/%{_lib}/libcap-ng.so.*.*.*
%ghost /%{_lib}/libcap-ng.so.0
%{_libdir}/libdrop_ambient.so.*.*.*
%ghost %{_libdir}/libdrop_ambient.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcap-ng.so
%{_libdir}/libcap-ng.la
%{_libdir}/libdrop_ambient.so
%{_libdir}/libdrop_ambient.la
%{_includedir}/cap-ng.h
%{_pkgconfigdir}/libcap-ng.pc
%{_aclocaldir}/cap-ng.m4
%{_mandir}/man3/capng_*.3*
%{_mandir}/man7/libdrop_ambient.7*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcap-ng.a
%{_libdir}/libdrop_ambient.a
%endif

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
%{bash_compdir}/libcap-ng
%if %{with cap_audit}
%attr(755,root,root) %{_bindir}/cap-audit
%{_mandir}/man8/cap-audit.8*
%endif

%if %{with python3}
%files -n python3-capng
%defattr(644,root,root,755)
%{py3_sitedir}/_capng.so
%{py3_sitedir}/capng.py
%{py3_sitedir}/__pycache__/capng.cpython-*.py[co]
%endif
