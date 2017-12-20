%define major 2
%define libname %mklibname unistring %{major}
%define devname %mklibname -d unistring

%global optflags %{optflags} -O3 --rtlib=compiler-rt
%define _disable_lto 1

Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.8
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
Patch0:		libunistring-0.9.8-check-for-__builtin_mul_overflow_p.patch
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
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure
%make

%install
%makeinstall_std

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
