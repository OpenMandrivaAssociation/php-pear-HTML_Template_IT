%define		_class		HTML
%define		_subclass	Template
%define		_status		stable
%define		_pearname	%{_class}_%{_subclass}_IT

Summary:	%{_pearname} - Integrated Templates
Name:		php-pear-%{_pearname}
Version:	1.2.1
Release:	%mkrel 1
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/HTML_Template_IT/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix

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

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_datadir}/pear/%{_class}/%{_subclass}/*.php
%{_datadir}/pear/packages/%{_pearname}.xml
