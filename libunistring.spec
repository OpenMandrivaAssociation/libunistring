%define name libunistring
%define version 0.9.3
%define release %mkrel 2
%define major 0
%define libname %mklibname unistring %major
%define develname %mklibname -d unistring
%define staticname %mklibname -s -d unistring

Summary: GNU Unicode string library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnu.org/software/libunistring/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: locales-fr
BuildRequires: texinfo

%description
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %libname
Group: System/Libraries
Summary: GNU Unicode string library

%description -n %libname
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %develname
Group: Development/C
Summary: GNU Unicode string library - development files
Requires: %libname = %version-%release
Provides: %name-devel = %version-%release

%description -n %develname
This library implements Unicode strings (in three flavours: UTF-8
strings, UTF-16 strings, UTF-32 strings), together with functions for
Unicode charactets (character names, classifications, properties) and
functions for string processing (formatted output, width, word breaks,
line breaks, normalization, case folding, regular expressions).

%package -n %staticname
Group: Development/C
Summary: GNU Unicode string library - static library
Requires: %develname = %version-%release
Provides: %name-static-devel = %version-%release

%description -n %staticname
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
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%post -n %develname
%_install_info %{name}.info

%preun -n %develname
%_remove_install_info %{name}.info

%files -n %libname
%defattr(-,root,root)
%doc AUTHORS NEWS README
%_libdir/libunistring.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc %_datadir/doc/%name/*.html
%_libdir/libunistring.la
%_libdir/libunistring.so
%_infodir/libunistring.info*
%_includedir/unistring
%_includedir/*.h


%files -n %staticname
%defattr(-,root,root)
%_libdir/libunistring.a
