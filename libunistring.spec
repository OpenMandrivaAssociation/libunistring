%define major 0
%define libname %mklibname unistring %{major}
%define develname %mklibname -d unistring

Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.3
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
BuildRequires:	locales-fr
BuildRequires:	texinfo

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

%package -n %{develname}
Group:		Development/C
Summary:	GNU Unicode string library - development files
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -s -d unistring} < %{version}-%{release}

%description -n %{develname}
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

%files -n %{libname}
%doc AUTHORS NEWS README
%{_libdir}/libunistring.so.%{major}*

%files -n %{develname}
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc %{_datadir}/doc/%{name}/*.html
%{_libdir}/libunistring.so
%{_infodir}/libunistring.info*
%{_includedir}/unistring
%{_includedir}/*.h

%changelog
* Wed May 02 2012 Götz Waschk <waschk@mandriva.org> 0.9.3-3mdv2012.0
+ Revision: 794976
- remove libtool archive
- yearly rebuild

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-2
+ Revision: 660290
- mass rebuild

* Sat Jul 10 2010 Götz Waschk <waschk@mandriva.org> 0.9.3-1mdv2011.0
+ Revision: 550288
- update to new version 0.9.3

* Mon Apr 12 2010 Götz Waschk <waschk@mandriva.org> 0.9.1.1-1mdv2010.1
+ Revision: 533662
- update to new version 0.9.1.1

* Mon Jul 27 2009 Götz Waschk <waschk@mandriva.org> 0.9.1-1mdv2010.0
+ Revision: 400508
- import libunistring

