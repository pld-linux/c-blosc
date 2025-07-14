#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	sse2		# SSE2 instructions without detection (detected SSE2/AVX parts are always enabled)

%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif

Summary:	Blosc: A blocking, shuffling and lossless compression library
Summary(pl.UTF-8):	Blosc: biblioteka blokowej, przetasowującej i bezstratnej kompresji
Name:		c-blosc
Version:	1.21.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/Blosc/c-blosc/releases
Source0:	https://github.com/Blosc/c-blosc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5097ee61dc1f25281811f5a55b91b2e4
Patch0:		%{name}-sse2.patch
URL:		https://www.blosc.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	lz4-devel
BuildRequires:	snappy-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blosc is a high performance compressor optimized for binary data. It
has been designed to transmit data to the processor cache faster than
the traditional, non-compressed, direct memory fetch approach via a
memcpy() OS call. Blosc is the first compressor (that the author is
aware of) that is meant not only to reduce the size of large datasets
on-disk or in-memory, but also to accelerate memory-bound
computations. It uses the blocking technique so as to reduce activity
in the memory bus as much as possible. In short, this technique works
by dividing datasets in blocks that are small enough to fit in caches
of modern processors and perform compression/decompression there. It
also leverages, if available, SIMD instructions (SSE2, AVX2) and
multi-threading capabilities of CPUs, in order to accelerate the
compression/decompression process to a maximum.

%description -l pl.UTF-8
Blosc to wysoko wydajny kompresor zoptymalizowany dla danych
binarnych. Został zaprojektowany do przesyłania danych do pamięci
podręcznej procesora szybciej, niż tradycyjne pobieranie danych
nieskompresowanych poprzez wywołanie memcpy(). Blosc wg wiedzy autora
jest pierwszym kompresorem pisanym z myślą nie tylko o zmniejszeniu
rozmiaru danych na dysku lub w pamięci, ale także przyspieszeniu
obliczeń w pamięci. Wykorzystuje technikę blokową aby możliwie
najbardziej zmniejszyć wykorzystanie szyny pamięciowej. W skrócie
technika ta działa na zasadzie podziału zbiorów danych na bloki
wystarczająco małe, aby mieścić się w pamięci podręcznej współczesnych
procesorów, i dokonywaniu w niej kompresji/dekompresji. Wykorzystuje
także (jeśli są dostępne) intrukcje SIMD oraz możliwości wielowątkowe
rpcesorów, aby maksymalnie przyspieszyć proces kompresji/dekompresji.

%package devel
Summary:	Header files for blosc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki blosc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for blosc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki blosc.

%package static
Summary:	Static blosc library
Summary(pl.UTF-8):	Statyczna biblioteka blosc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static blosc library.

%description static -l pl.UTF-8
Statyczna biblioteka blosc.

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DBUILD_STATIC=OFF} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DPREFER_EXTERNAL_LZ4=ON \
	-DPREFER_EXTERNAL_ZLIB=ON \
	-DPREFER_EXTERNAL_ZSTD=ON \
	%{?with_sse2:-DREQUIRE_SSE2=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE.rst FAQ.md README.md README_CHUNK_FORMAT.rst README_THREADED.rst RELEASE_NOTES.rst THANKS.rst
%attr(755,root,root) %{_libdir}/libblosc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblosc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblosc.so
%{_includedir}/blosc.h
%{_includedir}/blosc-export.h
%{_pkgconfigdir}/blosc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libblosc.a
%endif
