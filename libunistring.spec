# libunistring is used by libidn2, which is used by
# systemd, which is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 2
%define libname %mklibname unistring %{major}
%define devname %mklibname -d unistring
%define lib32name libunistring%{major}
%define dev32name libunistring-devel

%global optflags %{optflags} -O3

Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.10
Release:	5
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
Patch0:		libunistring-0.9.8-check-for-__builtin_mul_overflow_p.patch
Patch1:		libunistring-0.9.10-add-pkg-config-support.patch
#BuildRequires:	locales-fr
#BuildRequires:	texinfo

%description
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %{libname}
Group:		System/Libraries
Summary:	GNU Unicode string library

%description -n %{libname}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %{devname}
Group:		Development/C
Summary:	GNU Unicode string library - development files
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Group:		System/Libraries
Summary:	GNU Unicode string library (32-bit)

%description -n %{lib32name}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %{dev32name}
Group:		Development/C
Summary:	GNU Unicode string library - development files
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package includes the development files for %{name}.
%endif

%prep
%autosetup -p1
./autogen.sh --skip-gnulib

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files -n %{libname}
%{_libdir}/libunistring.so.%{major}*

%files -n %{devname}
%doc HACKING DEPENDENCIES THANKS
%doc AUTHORS NEWS README
%doc %{_datadir}/doc/%{name}/*.html
%{_libdir}/libunistring.so
%{_infodir}/libunistring.info*
%{_includedir}/unistring
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libunistring.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libunistring.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
