%define cvs 20030412
%define branch testing
Summary:	AIM transport module for Jabber
Summary(pl):	Modu³ transportowy AIM dla systemu Jabber
Name:		jabber-aim-transport
Version:	0
Release:	0.%{cvs}.1
License:	distributable
Group:		Applications/Communications
Source0:	http://aim-transport.jabberstudio.org/aim-transport-%{branch}-%{cvs}.tar.gz
# Source0-md5:	36da37c11b3addff7bde0d40b5f03514
URL:		http://www.jabber.org/
BuildRequires:	jabber-devel
%requires_eq	jabber
BuildRequires:	pth-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows Jabber to communicate with AIM servers.

%description -l pl
Modu³ ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami AIM.

%prep
%setup -qn aim-transport-%{branch}-%{cvs}

%build
%{__autoconf}
%configure --with-jabberd=/usr/include/jabberd/
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sysconfdir}}/jabberd

install src/aimtrans.so $RPM_BUILD_ROOT%{_libdir}/jabberd
install aim.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabberd/aimtrans.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -r /var/lock/subsys/jabberd ]; then
	if [ -r /var/lock/subsys/jabber-aimtrans ]; then
		/etc/rc.d/init.d/jabberd restart aimtrans >&2
	else
		echo "Run \"/etc/rc.d/init.d/jabberd start aimtrans\" to start AIM transport."
	fi
else
	echo "Run \"/etc/rc.d/init.d/jabberd start\" to start Jabber server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-aimtrans ]; then
		/etc/rc.d/init.d/jabberd stop aimtrans >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/jabberd/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabberd/*
