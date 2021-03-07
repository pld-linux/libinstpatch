#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	Library for processing digital sample based MIDI instrument "patch" files
Summary(pl.UTF-8):	Biblioteka do przetwarzania plików "wstawek" instrumentów MIDI opartych na próbkach cyfrowych
Name:		libinstpatch
Version:	1.1.5
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/swami/libinstpatch/releases
Source0:	https://github.com/swami/libinstpatch/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e2b4a0867a72e464aab0fd7dae9c1abe
Patch0:		%{name}-gtkdoc.patch
URL:		http://www.swamiproject.org/
BuildRequires:	cmake >= 2.6.3
BuildRequires:	glib2-devel >= 1:2.14
#BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libInstPatch stands for lib-Instrument-Patch and is a library for
processing digital sample based MIDI instrument "patch" files. The
types of files libInstPatch supports are used for creating instrument
sounds for wavetable synthesis. libInstPatch provides an object
framework (based on GObject) to load patch files into, which can then
be edited, converted, compressed and saved.

%description -l pl.UTF-8
libInstPatch to skrót od lib-Instrument-Patch i jest to biblioteka do
przetwarzania opartych na próbkach cyfrowych plików wstawek ("patchy")
instrumentów MIDI. Typy plików, jakie obsługuje libInstPatch, służą do
tworzenia dźwięków instrumentów do syntezy wavetable. libInstPatch
zapewnia szkielet obiektowy (oparty na GObject) do ładowania plików
próbek, które następnie mogą być modyfikowane, konwertowane,
kompresowane i zapisywane.

%package devel
Summary:	Header files for libinstpatch library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libinstpatch
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.14
Requires:	libsndfile-devel >= 1.0.0

%description devel
Header files for libinstpatch library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libinstpatch.

%package apidocs
Summary:	API documentation for libinstpatch library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libinstpatch
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libinstpatch library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libinstpatch.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{?with_apidocs:-DGTKDOC_ENABLED=ON}
#	-DINTROSPECTION_ENABLED=ON broken cmake support in 1.1.[35]

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gtkdocdir}/libinstpatch
cp -p build/docs/reference/libinstpatch/html/* $RPM_BUILD_ROOT%{_gtkdocdir}/libinstpatch
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md TODO.tasks
%attr(755,root,root) %{_libdir}/libinstpatch-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinstpatch-1.0.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinstpatch-1.0.so
%{_includedir}/libinstpatch-2
%{_pkgconfigdir}/libinstpatch-1.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libinstpatch
%endif
