# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: jcommon-serializer
Version: 0.3.0
Release: 3.1%{?dist}
Summary: JFree Java General Serialization Framework
License: LGPLv2+
Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/jfreereport/%{name}-%{version}.tar.gz
Source1: http://downloads.sourceforge.net/jfreereport/libserializer-1.0.0-OOo31.zip
URL: http://www.jfree.org/jfreereport/jcommon-serializer
BuildRequires: ant, java-devel, jpackage-utils, libbase >= 1.0.0
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils, libbase >= 1.0.0
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif
Patch1: jcommon-serializer-0.3.0-depends.patch

%description
Jcommon-serializer is a general serialization framework used by JFreeChart,
JFreeReport and other projects.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
Requires: %{name} = %{version}-%{release}
Requires: jpackage-utils
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch1 -p1 -b .depends
find . -name "*.jar" -exec rm -f {} \;
build-jar-repository -s -p lib libbase commons-logging-api
unzip -qq %{SOURCE1} -d serializer
cd serializer
mkdir -p lib
build-jar-repository -s -p lib libbase commons-logging-api

%build
ant compile javadoc
cd serializer
ant jar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -p serializer/build/lib/libserializer.jar $RPM_BUILD_ROOT%{_javadir}/libserializer.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc ChangeLog.txt licence-LGPL.txt README.txt
%{_javadir}/%{name}.jar
%{_javadir}/libserializer.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.3.0-3.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 0.3.0-3
- make javadoc no-arch when building as arch-dependant aot

* Mon Mar 16 2009 Caolan McNamara <caolanm@redhat.com> 0.3.0-2
- OOo tuned serializer

* Mon Mar 09 2009 Caolan McNamara <caolanm@redhat.com> 0.3.0-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2008 Caolan McNamara <caolanm@redhat.com> 0.2.0-3
- reshuffle

* Tue May 06 2008 Caolan McNamara <caolanm@redhat.com> 0.2.0-2
- take review notes

* Sat May 03 2008 Caolan McNamara <caolanm@redhat.com> 0.2.0-1
- initial fedora import
