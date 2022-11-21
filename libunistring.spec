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
%define sdevname %mklibname -d -s unistring
%define lib32name libunistring%{major}
%define dev32name libunistring-devel
%define sdev32name libunistring-static-devel

%global optflags %{optflags} -O3

Summary:	GNU Unicode string library
Name:		libunistring
Version:	1.1
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
Patch0:		libunistring-1.0-attribute-dealloc-clang.patch
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

%package -n %{sdevname}
Group:		Development/C
Summary:	GNU Unicode string library - static libraries
Requires:	%{devname} = %{version}-%{release}
Provides:	unistring-static-devel = %{EVRD}

%description -n %{sdevname}
This package includes the static libraries for %{name}.

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
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

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
