# libunistring is used by libidn2, which is used by
# systemd, which is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 5
%define oldlibname %mklibname unistring 5
%define libname %mklibname unistring
%define devname %mklibname -d unistring
%define sdevname %mklibname -d -s unistring
%define oldlib32name libunistring5
%define lib32name libunistring
%define dev32name libunistring-devel
%define sdev32name libunistring-static-devel

%global optflags %{optflags} -O3

Summary:	GNU Unicode string library
Name:		libunistring
Version:	1.4.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
Patch1:		libunistring-0.9.10-add-pkg-config-support.patch
Patch2:		libunistring-headers-clang.patch
BuildRequires:	slibtool
# Required for the configure check for iconv to succeed
# (which enables iconv support in libunistring, which is
# required by guile)
BuildRequires:	locales-extra-charsets
#BuildRequires:	texinfo
%if "%{lib32name}" == "%{name}"
%rename %{oldlib32name}
%endif
%if  "%{libname}" == "%{name}"
%rename %{oldlibname}
%endif

%description
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%if  "%{libname}" != "%{name}"
%package -n %{libname}
Group:		System/Libraries
Summary:	GNU Unicode string library
%rename %{oldlibname}
%endif

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

%package -n %{sdevname}
Group:		Development/C
Summary:	GNU Unicode string library - static libraries
Requires:	%{devname} = %{version}-%{release}
Provides:	unistring-static-devel = %{EVRD}

%description -n %{sdevname}
This package includes the static libraries for %{name}.

%if %{with compat32}
%if "%{lib32name}" != "%{name}"
%package -n %{lib32name}
Group:		System/Libraries
Summary:	GNU Unicode string library (32-bit)
%rename %{oldlib32name}

%description -n %{lib32name}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).
%endif

%package -n %{dev32name}
Group:		Development/C
Summary:	GNU Unicode string library - development files
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package includes the development files for %{name}.

%package -n %{sdev32name}
Group:		Development/C
Summary:	GNU Unicode string library - static libraries
Requires:	%{sdevname} = %{version}-%{release}
Requires:	%{dev32name} = %{version}-%{release}

%description -n %{sdev32name}
This package includes the static libraries for %{name}.
%endif

%prep
%autosetup -p1
rm -f m4/libtool.m4 m4/lt*.m4
./autogen.sh --skip-gnulib

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-static
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-static

%build
%if %{with compat32}
%make_build -C build32 LIBTOOL=slibtool
%endif
%make_build -C build LIBTOOL=slibtool

%install
%if %{with compat32}
%make_install -C build32 LIBTOOL=slibtool
%endif
%make_install -C build LIBTOOL=slibtool

%files -n %{libname}
%{_libdir}/libunistring.so.%{major}*

%files -n %{devname}
%doc HACKING DEPENDENCIES THANKS
%doc AUTHORS NEWS README
%doc %{_datadir}/doc/%{name}/*.html
%{_libdir}/libunistring.so
%doc %{_infodir}/libunistring.info*
%{_includedir}/unistring
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files -n %{sdevname}
%{_libdir}/libunistring.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libunistring.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libunistring.so
%{_prefix}/lib/pkgconfig/*.pc

%files -n %{sdev32name}
%{_prefix}/lib/lib*.a
%endif
