PowerDNS Authoritative Server
=============================
An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Authoritative Server.

Even though PowerDNS supports numerous backends, database servers are not (and
will not) be installed by this role.

This role is considered alpha quality at the moment, but issues and pull requests
are accepted.

Requirements
------------
An Ansible installation.

### For MySQL backend
If you want to use this role to automatic create user and database. You need to
fulfill these requirements

* You have to prepare root or privilege user that can create database and assign
permission to user. This privilege user must can connect to the database from
target machine.
* Configure **pdns_backends_mysql_credential** variable as describe below.

Role Variables
--------------
### pdns_backends
A dict that allows you configure the backends, this also installs the correct
packages for these backends. By default, no backends are installed and PowerDNS
will be unable to start.

### pdns_backends_mysql_credential
A dict that allows you to put privilege users to create mysql database and
assign user privilege to this database. Please read requirements before
configure this variable

### pdns_backends_sqlite3_databases
A list that has the paths to gsqlite3 databases. These databases will be
initialized by this role. Note that these will **not** be added to the PowerDNS
configuration. This should be done with pdns_backends, see the examples.

### pdns_config
A dict detailing the configuration of PowerDNS. You should not set the following
options here (other variables set these):
 * config-dir
 * set-uid
 * set-gid
 * any backend related options

See below for an example.

### pdns_config_dir
The directory where the configuration (`pdns.conf`) is stored. '/etc/powerdns'
by default.

### pdns_installation_type
How to install PowerDNS, either 'packages' or 'source'. 'packages' by default.

### pdns_repo_provider
When using 'packages' for pdns_installation_type, use operating system packages
('os') or the PowerDNS repository ('powerdns'). This is 'os' by default.

### pdns_repo_branch
 When installing from the PowerDNS repository, what branch should be installed?
Currently only 'master' and '40' (latest 4.0.x release) are supported.

### pdns_user
The user to run PowerDNS as, this is 'pdns' by default. This user is not (yet)
created (but the package might have done that for you).

### pdns_group
The group to run PowerDNS as, this is 'pdns' by default. This group is not (yet)
created (but the package might have done that for you).

Example Playbook
----------------
Run as a master using the bind backend (when you already have a named.conf):
```
- hosts: ns1.example.net
  roles:
    - role: PowerDNS.pdns
  vars:
    pdns_config:
      master: true
      local-address: '192.0.2.53'
    pdns_backends:
      bind:
        config: '/etc/named/named.conf'
```

Run the PowerDNS masterbranch from a package from repo.powerdns.com as a slave
with the MySQL backend:
```
- hosts: ns2.example.net
  roles:
    - role: PowerDNS.pdns
  vars:
    pdns_config:
      master: false
      slave: true
      local-address: '192.0.2.54'
    pdns_backends:
      gmysql:
        host: 192.0.2.120
        port: 3306
        user: powerdns
        password: P0w3rDn5
        dbname: pdns
    pdns_repo_provider: 'powerdns'
    pdns_repo_branch: 'master'
```

Run the PowerDNS master branch from a package from repo.powerdns.com as a master
with the MySQL backend and use the root user to initialize the database and database user:
```
- hosts: ns2.example.net
  roles:
    - role: PowerDNS.pdns
  vars:
    pdns_config:
      master: true
      slave: false
      local-address: '192.0.2.77'
    pdns_backends:
      gmysql:
        host: 192.0.2.120
        port: 3306
        user: powerdns
        password: P0w3rDn5
        dbname: pdns
    pdns_backends_mysql_credential:
      gmysql:
        priv_user: root
        priv_password: myrootpass
        priv_host:
          - "%"
    pdns_repo_provider: 'powerdns'
    pdns_repo_branch: 'master'
```

Note: when using pdns_backends_mysql_credential, the `host`, `user`, `dbname` and `password` options become mandatory.

Run as a master on port 5300, using two different PostgreSQL databases:
```
- hosts: ns2.example.net
  roles:
    - role: PowerDNS.pdns
  vars:
    pdns_config:
      master: true
      local-port: 5300
      local-address: '192.0.2.111'
    pdns_backends:
      'gpgsql:serverone':
        host: 192.0.2.124
        user: powerdns
        password: P0w3rDn5
        dbname: pdns2
      'gpgsql:otherserver':
        host: 192.0.2.125
        user: root
        password: root
        dbname: dns
```

Run with a single gsqlite3 backend and have the role create this database:
```
- hosts: ns4.example.net
  roles:
    - role: PowerDNS.pdns
  vars:
    database_name: '/var/lib/powerdns/db.sqlite'
    pdns_config:
      master: true
      slave: false
      local-address: '192.0.2.73'
    pdns_backends:
      gsqlite3:
        database: "{{ database_name }}"
        dnssec: yes
    pdns_backends_sqlite3_databases:
      - "{{ database_name }}"
```

License
-------

MIT
