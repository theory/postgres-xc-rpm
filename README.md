Postgres-XC RPM
===============

This project builds the Postgres-XC RPM.

    spectool -S -C SOURCES -g SPECS/postgresxc-1.1.spec
    rpmbuild -ba --define "_topdir `pwd`" SPECS/postgresxc-1.1.spec

Author
-------
* [David E. Wheeler](mailto:david.wheeler@iovation.com)
