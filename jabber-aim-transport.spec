%define cvs 20030412
%define branch testing
Summary:	AIM transport module for Jabber
Summary(pl):	Modu³ transportowy AIM dla systemu Jabber
Name:		jabber-aim-transport
Version:	0
Release:	0.%{cvs}.5
License:	distributable
Group:		Applications/Communications
Source0:	http://aim-transport.jabberstudio.org/aim-transport-%{branch}-%{cvs}.tar.gz
Source2:	jabber-aimtrans.init
Source3:	jabber-aimtrans.sysconfig
Source4:	aimtrans.xml
# Source0-md5:	36da37c11b3addff7bde0d40b5f03514
URL:		http://www.jabber.org/
BuildRequires:	autoconf
BuildRequires:	jabberd14-devel
BuildRequires:	pth-devel
PreReq:		rc-scripts
Requires(post):	jabber-common
Requires(post):	perl-base
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
	--with-jabberd=/usr/include/jabberd14/
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
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in the config file..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/aimtrans.xml
	fi
fi

/sbin/chkconfig --add jabber-aimtrans
if [ -r /var/lock/subsys/jabber-aimtrans ]; then
	/etc/rc.d/init.d/jabber-aimtrans restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-aimtrans start\" to start Jabber aim transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-aimtrans ]; then
		/etc/rc.d/init.d/jabber-aimtrans stop >&2
	fi
	/sbin/chkconfig --del jabber-aimtrans
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/jabberd14/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jabber-aimtrans
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jabber-aimtrans
