%define		_class		HTML
%define		_subclass	Template
%define		upstream_name	%{_class}_%{_subclass}_IT

Name:		php-pear-%{upstream_name}
Version:	1.3.0
Release:	%mkrel 3
Summary:	Integrated Templates
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/HTML_Template_IT/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
HTML_Template_IT: Simple template API. The Isotemplate API is somewhat
tricky for a beginner although it is the best one you can build.
template::parse() [phplib template = Isotemplate] requests you to name
a source and a target where the current block gets parsed into. Source
and target can be block names or even handler names. This API gives
you a maximum of fexibility but you always have to know what you do
which is quite unusual for PHP skripter like me. I noticed that I do
not any control on which block gets parsed into which one. If all
blocks are within one file, the script knows how they are nested and
in which way you have to parse them. IT knows that inner1 is a child
of block2, there's no need to tell him about this. Features:
 - Nested blocks,
 - Include external file,
 - Custom tags format (default {mytag}).

HTML_Template_ITX: With this class you get the full power of the
phplib template class. You may have one file with blocks in it but you
have as well one main file and multiple files one for each block. This
is quite useful when you have user configurable websites. Using blocks
not in the main template allows you to modify some parts of your
layout easily.

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
