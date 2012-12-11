%define modname bloomy
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A97_%{modname}.ini

Summary:	Extension implementing a Bloom filter
Name:		php-%{modname}
Version:	0.1.0
Release:	%mkrel 13
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/bloomy/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		bloomy-0.1.0-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension implements a Bloom filter, which is a space-efficient
probabilistic data structure that is used to test whether an element is a
member of a set.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-13mdv2012.0
+ Revision: 797128
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-12
+ Revision: 761203
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-11
+ Revision: 696396
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-10
+ Revision: 695368
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9
+ Revision: 646615
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2011.0
+ Revision: 629768
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2011.0
+ Revision: 628070
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2011.0
+ Revision: 600464
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2011.0
+ Revision: 588746
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2010.1
+ Revision: 514520
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2010.1
+ Revision: 485341
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2010.1
+ Revision: 468147
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.0
+ Revision: 452902
- import php-bloomy


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.0
- initial Mandriva package
