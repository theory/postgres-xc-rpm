# This is a macro to be used with find_lang and other stuff
%define majorversion 1.1
%define packageversion 11
%define oname postgresxc
%define sname pgxc
%define	pgxcbaseinstdir	/usr/%{sname}-%{majorversion}
%define user  postgres
%define group postgres
%define gid   26
%define uid   26

Summary:	Postgres-XC client programs and libraries
Name:		%{oname}%{packageversion}
Version:	%{majorversion}
Release:	1iov%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://postgres-xc.sourceforge.net/

Source0:	http://hivelocity.dl.sourceforge.net/project/postgres-xc/Version_%{majorversion}/pgxc-v%{majorversion}.tar.gz
Source1:	%{oname}.init

Buildrequires:	perl python-devel glibc-devel bison flex gcc make
Requires:	/sbin/ldconfig initscripts

BuildRequires: perl-ExtUtils-Embed
BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4
BuildRequires:	openssl-devel
BuildRequires:	libxml2-devel libxslt-devel
BuildRequires:	uuid-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	%{oname}

%description
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent Postgres-XC cluster solution. It is a collection if
tightly coupled database components which can be installed in more than one
hardware or virtual machines.

Write-scalable means Postgres-XC can be configured with as many database
servers as you want and handle many more writes (updating SQL statements)
compared to what a single database server can not do.

Multi-master means you can have more than one database server that clients
connect to which provide a single, consistent cluster-wide view of the
database.

Synchronous means any database update from any database server is immediately
visible to any other transactions running on different masters.

Transparent means you (and your applications) do not have to worry about how
your data is stored in more than one database servers internally.

You can configure Postgres-XC to run on multiple servers. Your data is stored
in a distributed way, that is, partitioned or replicated, as chosen by you for
each table. When you issue queries, Postgres-XC determines where the target
data is stored and issues corresponding queries to servers containing the
target data.

%pre
%{_sbindir}/groupadd -g %{gid} %{group} >/dev/null 2>&1 || :
%{_sbindir}/useradd -M -N -g %{group} -d %{prefix}/%{name} \
    -c "Postgres-XC Server" -u %{uid} %{user} >/dev/null 2>&1 || :

%post
chkconfig --add %{oname}%{majorversion}
/sbin/ldconfig

%prep
%setup -q -n postgres-xc

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

export LIBNAME=%{_lib}

./configure --disable-rpath \
	--prefix=%{pgxcbaseinstdir} \
	--includedir=%{pgxcbaseinstdir}/include \
	--mandir=%{pgxcbaseinstdir}/share/man \
	--datadir=%{pgxcbaseinstdir}/share \
	--with-perl \
	--with-python \
	--with-openssl \
	--with-ossp-uuid \
	--with-libxml \
	--with-libxslt \
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/%{sname} \
	--docdir=%{_docdir}/%{sname}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
make %{?_smp_mflags} -C contrib/uuid-ossp all

%install
%{__rm} -rf $RPM_BUILD_ROOT

rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{pgxcbaseinstdir}/share/extensions/
make -C contrib DESTDIR=%{buildroot} install
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install

install -d %{buildroot}/etc/rc.d/init.d
sed 's/^PGXCVERSION=.*$/PGXCVERSION=%{version}/' <%{SOURCE1} > %{oname}.init
install -m 755 %{oname}.init %{buildroot}/etc/rc.d/init.d/%{oname}-%{majorversion}

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/%{sname}/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/%{sname}/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/%{sname}/%{majorversion}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) /etc/rc.d/init.d/%{oname}-%{majorversion}
%attr (755,root,root) %dir /etc/sysconfig/%{sname}
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES 
%doc COPYRIGHT doc/bug.template
%{pgxcbaseinstdir}/
%{_docdir}/%{sname}

%changelog
* Fri Jan 17 2014 David E. Wheeler <david@justatheory.com> - 1.1-1PGDG
- Initial cut for 1.1.
