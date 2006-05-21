%define cvs 20040131
%define branch stable
Summary:	AIM transport module for Jabber
Summary(pl):	Modu³ transportowy AIM dla systemu Jabber
Name:		jabber-aim-transport
Version:	0
Release:	0.%{cvs}.1
License:	distributable
Group:		Applications/Communications
Source0:	http://aim-transport.jabberstudio.org/aim-transport-%{branch}-%{cvs}b.tar.gz
# Source0-md5:	804469a50824691adcfa2cec71dbf6df
Source2:	jabber-aimtrans.init
Source3:	jabber-aimtrans.sysconfig
Source4:	aimtrans.xml
URL:		http://www.jabber.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	jabberd14-devel
BuildRequires:	pth-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
%requires_eq	jabberd14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with AIM servers.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami AIM.

%prep
%setup -qn aim-transport-%{branch}-%{cvs}

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-jabberd=/usr/include/jabberd14
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/jabberd14,%{_sysconfdir}/jabber} \
	$RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install src/aimtrans.so $RPM_BUILD_ROOT%{_libdir}/jabberd14
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-aimtrans
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jabber-aimtrans
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/aimtrans.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in the config file..."
		%{__sed} -i -e "s/>secret</>$SECRET</" %{_sysconfdir}/jabber/aimtrans.xml
	fi
fi

/sbin/chkconfig --add jabber-aimtrans
%service jabber-aimtrans restart "Jabber aim transport"

%preun
if [ "$1" = "0" ]; then
	%service jabber-aimtrans stop
	/sbin/chkconfig --del jabber-aimtrans
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/jabberd14/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-aimtrans
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jabber-aimtrans
