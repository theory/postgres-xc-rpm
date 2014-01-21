%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

# This is a macro to be used with find_lang and other stuff
%define majorversion 1.1
%define packageversion 11
%define pgmajorversion 9.2
%define oname postgresxc
%define sname pgxc
%define	pgbaseinstdir	/usr/%{sname}-%{majorversion}
%define uname  postgres
%define gname postgres
%define gid   26
%define uid   26

%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}

Summary:	Postgres-XC client programs and libraries
Name:		%{oname}%{packageversion}
Version:	%{majorversion}.0
Release:	1iov%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://postgres-xc.sourceforge.net/

Source0:	http://hivelocity.dl.sourceforge.net/project/postgres-xc/Version_%{majorversion}/pgxc-v%{majorversion}.tar.gz
Source1:	%{oname}.init
Source2:	%{oname}-%{majorversion}-libs.conf
Source3:	Makefile.regress
Source4:	filter-requires-perl-Pg.sh
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source8:	%{oname}.pam

Patch1:		rpm-pgxc.patch
Patch2:		%{oname}-logging.patch
Patch3:		%{oname}-perl-rpath.patch
Patch4:		%{oname}-prefer-ncurses.patch

Buildrequires: gcc make	perl glibc-devel bison flex openjade
Requires:	/sbin/ldconfig initscripts

%if %plperl
BuildRequires: perl-ExtUtils-Embed
BuildRequires: perl(ExtUtils::MakeMaker)
%endif

%if %plpython
BuildRequires:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %uuid
BuildRequires:	uuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

Requires:	%{name}-libs = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	%{oname}

%description
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent PostgreSQL cluster solution. It is a collection if
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

%package libs
Summary:	The shared libraries required for any Postgres-XC clients
Group:		Applications/Databases
Provides:	libpq.so
Provides:	postgresxc-libs

%description libs
The postgresxc93-libs package provides the essential shared libraries for any
Postgres-XC client program or interface. You will need to install this package
to use any other Postgres-XC package or any clients that need to connect to a
Postgres-XC server.

%package server
Summary:	The programs needed to create and run a Postgres-XC server
Group:		Applications/Databases
Requires:	/usr/sbin/useradd /sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Provides:	postgresxc-server

%description server

The postgresxc93-server package includes the programs needed to create and run
a Postgres-XC server, which will in turn allow you to create and maintain
Postgres-XC databases. Postgres-XC is an open source project to provide a
write-scalable, synchronous multi-master, transparent PostgreSQL cluster
solution. It is a collection if tightly coupled database components which can
be installed in more than one hardware or virtual machines. You should install
postgresxc93-server if you want to create and maintain your own Postgres-XC
databases and/or your own Postgres-XC server. You also need to install the
postgresxc package.

%package docs
Summary:	Extra documentation for Postgres-XC
Group:		Applications/Databases
Provides:	postgresxc-docs

%description docs
The postgresxc93-docs package includes the SGML source for the Postgres-XC
documentation as well as some extra documentation. Install this package if you
want to help with the Postgres-XC documentation project, or if you want to
generate printed documentation. This package also includes HTML version of the
documentation.

%package contrib
Summary:	Contributed modules and binaries distributed with Postgres-XC
Group:		Applications/Databases
Requires:	%{name} = %{version}
Provides:	postgresxc-contrib

%description contrib
The postgresxc93-contrib package contains contributed packages that are
included in the Postgres-XC distribution.

%package devel
Summary:	Postgres-XC development header files and libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	postgresxc-devel

%description devel
The postgresxc93-devel package contains the header files and libraries needed
to compile C or C++ applications which will directly interact with a
Postgres-XC database management server and the ecpg Embedded C Postgres
preprocessor. You need to install this package if you want to develop
applications which will interact with a Postgres-XC server.

%if %plperl
%package plperl
Summary:	The Perl procedural language for Postgres-XC
Group:		Applications/Databases
Requires:	%{name}-server = %{version}-%{release}
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Provides:	postgresxc-plperl

%description plperl
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent PostgresSQL cluster solution. The
postgresxc93-plperl package contains the PL/Perl language for the backend.
%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for Postgres-XC
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Provides:	postgresxc-plpython

%description plpython
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent PostgresSQL cluster solution. The
postgresxc93-plpython package contains the PL/Python language for the backend.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for Postgres-XC
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Provides:	postgresxc-pltcl

%description pltcl
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent PostgresSQL cluster solution. The postgresxc93-pltcl
package contains the PL/Tcl language for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with Postgres-XC
Group:		Applications/Databases
Requires:	%{name}-server = %{version}-%{release}
Provides:	postgresxc-test

%description test
Postgres-XC is an open source project to provide a write-scalable, synchronous
multi-master, transparent PostgresSQL cluster solution. The postgresxc-test
package includes the sources and pre-built binaries of various tests for the
Postgres-XC database management system, including regression tests and
benchmarks.
%endif

%define __perl_requires %{SOURCE4}

%prep
%setup -q -n postgres-xc
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

export LIBNAME=%{_lib}

./configure --disable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
    --datarootdir=%{pgbaseinstdir}/share \
    --libdir=%{pgbaseinstdir}/lib \
%if %beta
    --enable-debug \
    --enable-cassert \
%endif
%if %plperl
    --with-perl \
%endif
%if %plpython
    --with-python \
%endif
%if %pltcl
    --with-tcl \
    --with-tclconfig=%{_libdir} \
%endif
%if %ssl
    --with-openssl \
%endif
%if %pam
    --with-pam \
%endif
%if %kerberos
    --with-krb5 \
    --with-gssapi \
    --with-includes=%{kerbdir}/include \
    --with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
    --enable-nls \
%endif
%if !%intdatetimes
    --disable-integer-datetimes \
%endif
%if %disablepgfts
    --disable-thread-safety \
%endif
%if %uuid
    --with-ossp-uuid \
%endif
%if %xml
    --with-libxml \
    --with-libxslt \
%endif
%if %ldap
    --with-ldap \
%endif
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --sysconfdir=/etc/sysconfig/%{sname} \
    --docdir=%{_docdir}/%{sname}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C doc all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
    pushd src/test/regress
    make all
    cp ../../../contrib/spi/refint.so .
    cp ../../../contrib/spi/autoinc.so .
    make MAX_CONNECTIONS=5 check
    make clean
    popd
    pushd src/pl
    make MAX_CONNECTIONS=5 check
    popd
    pushd contrib
    make MAX_CONNECTIONS=5 check
    popd
%endif

%if %test
    pushd src/test/regress
    make all
    popd
%endif

%install
%{__rm} -rf %{buildroot}

make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{pgbaseinstdir}/share/extensions/
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
    i386 | x86_64 | ppc | ppc64 | s390 | s390x)
        mv %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
        install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/
        mv %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
        install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/
        mv %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
        install -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/
        ;;
    *)
    ;;
esac

install -d %{buildroot}/etc/rc.d/init.d
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE1} > %{oname}.init
install -m 755 %{oname}.init %{buildroot}/etc/rc.d/init.d/%{oname}-%{majorversion}

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE8} %{buildroot}/etc/pam.d/%{oname}%{packageversion}
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/%{sname}/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/%{sname}/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/%{sname}/%{majorversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
install -d -m 755 %{buildroot}%{pgbaseinstdir}/share/
install -m 700 %{SOURCE2} %{buildroot}%{pgbaseinstdir}/share/

%if %test
    # tests. There are many files included here that are unnecessary,
    # but include them anyway for completeness.  We replace the original
    # Makefiles, however.
    mkdir -p %{buildroot}%{pgbaseinstdir}/lib/test
    cp -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
    install -m 0755 contrib/spi/refint.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
    install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
    pushd  %{buildroot}%{pgbaseinstdir}/lib/test/regress
    strip *.so
    rm -f GNUmakefile Makefile *.o
    chmod 0755 pg_regress regress.so
    popd
    cp %{SOURCE3} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
    chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgbaseinstdir}/share/doc/html
mv doc/src/sgml/html doc
mkdir -p %{buildroot}%{pgbaseinstdir}/share/man/
mv doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7  %{buildroot}%{pgbaseinstdir}/share/man/
rm -rf %{buildroot}%{_docdir}/%{sname}

# Fix some file locations.

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

%if %nls
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetxlog-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%if %plperl
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgmajorversion}
%if %plpython
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang > pg_plpython.lst
%endif
%if %pltcl
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}
%endif

cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst
cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang > pg_devel.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetxlog-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang > pg_server.lst

%pre server
%{_sbindir}/groupadd -g %{gid} %{gname} >/dev/null 2>&1 || :
%{_sbindir}/useradd -M -N -g %{gname} -d %{prefix}/%{name} \
    -c "Postgres-XC Server" -u %{uid} %{uname} >/dev/null 2>&1 || :
touch /var/log/%{sname}
chown %{uname}:%{gname} /var/log/%{sname}
chmod 0700 /var/log/%{sname}

%post server
chkconfig --add %{oname}-%{majorversion}
/sbin/ldconfig
# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/%{sname}/%{majorversion}/data
export PGDATA" >  /var/lib/%{sname}/.bash_profile
chown %{uname}: /var/lib/%{sname}/.bash_profile

%preun server
if [ $1 = 0 ] ; then
    /sbin/service %{oname}-%{majorversion} condstop >/dev/null 2>&1
    chkconfig --del %{oname}-%{majorversion}
fi

%postun server
/sbin/ldconfig
if [ $1 -ge 1 ]; then
  /sbin/service %{oname}-%{majorversion} condrestart >/dev/null 2>&1
fi

%if %plperl
%post   -p /sbin/ldconfig	plperl
%postun	-p /sbin/ldconfig   plperl
%endif

%if %plpython
%post   -p /sbin/ldconfig	plpython
%postun	-p /sbin/ldconfig   plpython
%endif

%if %pltcl
%post   -p /sbin/ldconfig	pltcl
%postun	-p /sbin/ldconfig   pltcl
%endif

%if %test
%post test
chown -R %{uname}:%{gname} /usr/share/%{sname}/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql %{sname}-psql %{pgbaseinstdir}/bin/psql 930
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb  %{sname}-clusterdb  %{pgbaseinstdir}/bin/clusterdb 930
%{_sbindir}/update-alternatives --install /usr/bin/createdb   %{sname}-createdb   %{pgbaseinstdir}/bin/createdb 930
%{_sbindir}/update-alternatives --install /usr/bin/createlang %{sname}-createlang %{pgbaseinstdir}/bin/createlang 930
%{_sbindir}/update-alternatives --install /usr/bin/createuser %{sname}-createuser %{pgbaseinstdir}/bin/createuser 930
%{_sbindir}/update-alternatives --install /usr/bin/dropdb     %{sname}-dropdb     %{pgbaseinstdir}/bin/dropdb 930
%{_sbindir}/update-alternatives --install /usr/bin/droplang   %{sname}-droplang   %{pgbaseinstdir}/bin/droplang 930
%{_sbindir}/update-alternatives --install /usr/bin/dropuser   %{sname}-dropuser   %{pgbaseinstdir}/bin/dropuser 930
%{_sbindir}/update-alternatives --install /usr/bin/pg_basebackup    %{sname}-pg_basebackup    %{pgbaseinstdir}/bin/pg_basebackup 930
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump    %{sname}-pg_dump    %{pgbaseinstdir}/bin/pg_dump 930
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall %{sname}-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall 930
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore %{sname}-pg_restore %{pgbaseinstdir}/bin/pg_restore 930
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb  %{sname}-reindexdb  %{pgbaseinstdir}/bin/reindexdb 930
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb   %{sname}-vacuumdb   %{pgbaseinstdir}/bin/vacuumdb 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1  %{sname}-clusterdbman     %{pgbaseinstdir}/share/man/man1/clusterdb.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1   %{sname}-createdbman   %{pgbaseinstdir}/share/man/man1/createdb.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 %{sname}-createlangman    %{pgbaseinstdir}/share/man/man1/createlang.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 %{sname}-createuserman    %{pgbaseinstdir}/share/man/man1/createuser.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1     %{sname}-dropdbman        %{pgbaseinstdir}/share/man/man1/dropdb.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   %{sname}-droplangman   %{pgbaseinstdir}/share/man/man1/droplang.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   %{sname}-dropuserman   %{pgbaseinstdir}/share/man/man1/dropuser.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_basebackup.1    %{sname}-pg_basebackupman    %{pgbaseinstdir}/share/man/man1/pg_basebackup.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    %{sname}-pg_dumpman    %{pgbaseinstdir}/share/man/man1/pg_dump.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 %{sname}-pg_dumpallman    %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 %{sname}-pg_restoreman    %{pgbaseinstdir}/share/man/man1/pg_restore.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1       %{sname}-psqlman          %{pgbaseinstdir}/share/man/man1/psql.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  %{sname}-reindexdbman     %{pgbaseinstdir}/share/man/man1/reindexdb.1 930
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   %{sname}-vacuumdbman   %{pgbaseinstdir}/share/man/man1/vacuumdb.1 930

%post libs
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/%{oname}-pgdg-libs.conf   %{sname}-ld-conf        %{pgbaseinstdir}/share/%{oname}-%{majorversion}-libs.conf 930
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
  if [ "$1" -eq 0 ]
   then
    # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
    %{_sbindir}/update-alternatives --remove %{sname}-psql		%{pgbaseinstdir}/bin/psql
    %{_sbindir}/update-alternatives --remove %{sname}-clusterdb	%{pgbaseinstdir}/bin/clusterdb
    %{_sbindir}/update-alternatives --remove %{sname}-clusterdbman	%{pgbaseinstdir}/share/man/man1/clusterdb.1
    %{_sbindir}/update-alternatives --remove %{sname}-createdb		%{pgbaseinstdir}/bin/createdb
    %{_sbindir}/update-alternatives --remove %{sname}-createdbman	%{pgbaseinstdir}/share/man/man1/createdb.1
    %{_sbindir}/update-alternatives --remove %{sname}-createlang	%{pgbaseinstdir}/bin/createlang
    %{_sbindir}/update-alternatives --remove %{sname}-createlangman	%{pgbaseinstdir}/share/man/man1/createlang.1
    %{_sbindir}/update-alternatives --remove %{sname}-createuser	%{pgbaseinstdir}/bin/createuser
    %{_sbindir}/update-alternatives --remove %{sname}-createuserman	%{pgbaseinstdir}/share/man/man1/createuser.1
    %{_sbindir}/update-alternatives --remove %{sname}-dropdb		%{pgbaseinstdir}/bin/dropdb
    %{_sbindir}/update-alternatives --remove %{sname}-dropdbman	%{pgbaseinstdir}/share/man/man1/dropdb.1
    %{_sbindir}/update-alternatives --remove %{sname}-droplang		%{pgbaseinstdir}/bin/droplang
    %{_sbindir}/update-alternatives --remove %{sname}-droplangman	%{pgbaseinstdir}/share/man/man1/droplang.1
    %{_sbindir}/update-alternatives --remove %{sname}-dropuser		%{pgbaseinstdir}/bin/dropuser
    %{_sbindir}/update-alternatives --remove %{sname}-dropuserman	%{pgbaseinstdir}/share/man/man1/dropuser.1
    %{_sbindir}/update-alternatives --remove %{sname}-pg_basebackup	%{pgbaseinstdir}/bin/pg_basebackup
    %{_sbindir}/update-alternatives --remove %{sname}-pg_dump		%{pgbaseinstdir}/bin/pg_dump
    %{_sbindir}/update-alternatives --remove %{sname}-pg_dumpall	%{pgbaseinstdir}/bin/pg_dumpall
    %{_sbindir}/update-alternatives --remove %{sname}-pg_dumpallman	%{pgbaseinstdir}/share/man/man1/pg_dumpall.1
    %{_sbindir}/update-alternatives --remove %{sname}-pg_basebackupman	%{pgbaseinstdir}/share/man/man1/pg_basebackup.1
    %{_sbindir}/update-alternatives --remove %{sname}-pg_dumpman	%{pgbaseinstdir}/share/man/man1/pg_dump.1
    %{_sbindir}/update-alternatives --remove %{sname}-pg_restore	%{pgbaseinstdir}/bin/pg_restore
    %{_sbindir}/update-alternatives --remove %{sname}-pg_restoreman	%{pgbaseinstdir}/share/man/man1/pg_restore.1
    %{_sbindir}/update-alternatives --remove %{sname}-psqlman		%{pgbaseinstdir}/share/man/man1/psql.1
    %{_sbindir}/update-alternatives --remove %{sname}-reindexdb	%{pgbaseinstdir}/bin/reindexdb
    %{_sbindir}/update-alternatives --remove %{sname}-reindexdbman	%{pgbaseinstdir}/share/man/man1/reindexdb.1
    %{_sbindir}/update-alternatives --remove %{sname}-vacuumdb		%{pgbaseinstdir}/bin/vacuumdb
    %{_sbindir}/update-alternatives --remove %{sname}-vacuumdbman	%{pgbaseinstdir}/share/man/man1/vacuumdb.1
  fi

%postun libs
if [ "$1" -eq 0 ]
  then
    %{_sbindir}/update-alternatives --remove %{sname}-ld-conf          %{pgbaseinstdir}/share/%{oname}-%{majorversion}-libs.conf
    /sbin/ldconfig
fi

%clean
%{__rm} -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createlang
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/droplang
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
#%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_receivexlog
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/gtm
%{pgbaseinstdir}/bin/gtm_ctl
%{pgbaseinstdir}/bin/gtm_proxy
%{pgbaseinstdir}/bin/initgtm
%{pgbaseinstdir}/bin/makesgml
%{pgbaseinstdir}/bin/pgxc_clean
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createlang.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/droplang.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
#%{pgbaseinstdir}/share/man/man1/pg_isready.*
%{pgbaseinstdir}/share/man/man1/pg_receivexlog.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
#%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/chkpass.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/dummy_seclabel.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pgrowlocks.so
#%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/sslinfo.so
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/pg_upgrade_support.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/timetravel.so
%{pgbaseinstdir}/lib/unaccent.so
#%{pgbaseinstdir}/lib/worker_spi.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/extension/adminpack*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/chkpass*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore*
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree*
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
#%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%{pgbaseinstdir}/share/extension/sslinfo*
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/test_parser*
%{pgbaseinstdir}/share/extension/timetravel*
%{pgbaseinstdir}/share/extension/tsearch2*
%{pgbaseinstdir}/share/extension/unaccent*
%if %uuid
%{pgbaseinstdir}/share/extension/uuid-ossp*
%endif
%{pgbaseinstdir}/share/extension/xml2*
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_upgrade
#%{pgbaseinstdir}/bin/pg_xlogdump
%{pgbaseinstdir}/share/man/man1/oid2name.1
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.1
%{pgbaseinstdir}/share/man/man1/pg_standby.1
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.1
%{pgbaseinstdir}/share/man/man1/pg_test_timing.1
%{pgbaseinstdir}/share/man/man1/pg_upgrade.1
#%{pgbaseinstdir}/share/man/man1/pg_xlogdump.1
%{pgbaseinstdir}/share/man/man1/pgbench.1
%{pgbaseinstdir}/share/man/man1/vacuumlo.1



%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %{pgbaseinstdir}/share/%{oname}-%{majorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%config(noreplace) /etc/rc.d/init.d/%{oname}-%{majorversion}
%if %pam
%config(noreplace) /etc/pam.d/%{oname}%{packageversion}
%endif
%attr (755,root,root) %dir /etc/sysconfig/%{sname}
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/postgres.description
%{pgbaseinstdir}/share/postgres.shdescription
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/plpgsql.so
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*
%{pgbaseinstdir}/lib/test_parser.so
%{pgbaseinstdir}/lib/tsearch2.so

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/%{sname}
%attr(700,postgres,postgres) %dir /var/lib/%{sname}/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/%{sname}/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/%{sname}/%{majorversion}/backups
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/conversion_create.sql
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
#%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pgxs/*
#%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plperl.so
%{pgbaseinstdir}/share/extension/plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/bin/pltcl_delmod
%{pgbaseinstdir}/bin/pltcl_listmod
%{pgbaseinstdir}/bin/pltcl_loadmod
%{pgbaseinstdir}/share/unknown.pltcl
%{pgbaseinstdir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plpython*.so
%{pgbaseinstdir}/share/extension/plpython2u*
%{pgbaseinstdir}/share/extension/plpythonu*
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Fri Jan 17 2014 David E. Wheeler <david@justatheory.com> - 1.1-1PGDG
- Initial cut for 1.1.
