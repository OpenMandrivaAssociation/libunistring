%define major	0
%define libname %mklibname unistring %{major}
%define devname %mklibname -d unistring
%define	static	%mklibname -s -d unistring

Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.3
Release:	4
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libunistring/
BuildRequires:	locales-fr
BuildRequires:	texinfo

%description
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n	%{libname}
Group:		System/Libraries
Summary:	GNU Unicode string library

%description -n	%{libname}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n	%{devname}
Group:		Development/C
Summary:	GNU Unicode string library - development files
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n	%{static}
Group:		Development/C
Summary:	GNU Unicode string library - static library
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{static}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%prep
%setup -q

%build
%configure2_5x 
%make


%install
%makeinstall_std

%files -n %{libname}
%doc AUTHORS NEWS README
%{_libdir}/libunistring.so.%{major}*

%files -n %{devname}
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc %{_datadir}/doc/%{name}/*.html
%{_libdir}/libunistring.so
%{_infodir}/libunistring.info*
%{_includedir}/unistring
%{_includedir}/*.h

%files -n %{static}
%{_libdir}/libunistring.a
