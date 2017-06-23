PowerDNS Authoritative Server Role
==================================

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Authoritative Server.

Even though PowerDNS supports numerous backends, database servers are not (and
will not) be installed by this role.

Requirements
------------

An Ansible 2.0 or higher installation.

### For MySQL backend
If you want to use this role to automatic create user and database. You need to
fulfill these requirements

* You have to prepare root or privilege user that can create database and assign
permission to user. This privilege user must can connect to the database from
target machine.
* Configure **pdns_backends_mysql_credential** variable as describe below.

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

    pdns_install_repo: ""

By default, PowerDNS is installed from the os default repositories.
You can install the PowerDNS packages from the official PowerDNS repository
ovveriding the `pdns_install_repo` variable as follows:

    # Install PowerDNS from the master branch
    - hosts: all
      roles:
        - { role: PowerDNS.pdns,
            pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"

    # Install the PowerDNS package from the '40' branch 
    - hosts: all
      roles:
        - { role: PowerDNS.pdns,
            pdns_install_repo: "{{ pdns_auth_powerdns_repo_40 }}"

The roles also supports custom repositories

    - hosts: all
      vars:
        pdns_install_repo:
          apt_repo_origin: "my.repo.com"  # used to pin the pdns to the provided repository
          apt_repo: "deb http://my.repo.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/pdns main"
          gpg_key: "http://my.repo.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
          gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
          yum_repo_baseurl: "http://my.repo.com/centos/$basearch/$releasever/pdns"
          yum_repo_name: "powerdns"       # used to select only the pdns packages coming from this repo
      roles:
        - { role: PowerDNS.pdns }

If targeting only a specific platform (e.g. Debian) it's not needed to provide other platform (e.g. yum) repositories information.

    pdns_install_epel: True

On RedHat-like system, by default the role installs EPEL.
EPEL is needed to satisfy some PowerDNS dependencies like `protobuf`.
To skip EPEL installation set `pdns_install_epel` to `False`.

    pdns_package_name: "{{ default_pdns_package_name }}"

The name of the PowerDNS Server package, `pdns` on RedHat-like systems and `pdns-server` on Debian-like systems.

    pdns_user: pdns
    pdns_group: pdns

The user and group the PowerDNS will run as.
**NOTE**: This role does not create any user or group as we assume that they're created
by the package or other roles.

    pdns_service_name: "pdns"

Name of the PowerDNS service.

    pdns_flush_handlers: False

Force the execution of the flushing of the handlers at the end of the role.
**NOTE:** This is required, for instance, if using this role to do configure PowerDNS virtualhosting 
(https://doc.powerdns.com/md/authoritative/running/#starting-virtual-instances-with-system)

    pdns_config_dir: "{{ default_pdns_config_dir }}"
    pdns_config_file: "pdns.conf"

The PowerDNS configuration files and directories.

    pdns_config: {}

A dict containing all configuration options, except for backend
configuration and the `config-dir`, `setuid` and `setgid` directives.
For example:

    pdns_config:
      master: yes
      slave: no
      local-address: '192.0.2.53'
      local-ipv6: '2001:DB8:1::53'
      local-port: '5300'

configures PowerDNS to listen incoming DNS requests on port 5300.

    pdns_backends:
      bind:
        config: '/dev/null'

A dict with all the backends you'd like to have. You can use
multiple backends of the same kind by using the `{backend}:{instance_name}` syntax.
For example:

    pdns_backends:
      'gmysql:one':
        'user': root
        'host': 127.0.0.1
        'password': root
        'dbname': pdns
      'gmysql:two':
        'user': pdns_user
        'host': 192.0.2.15
        'password': my_password
        'dbname': dns
      'bind':
        'config': '/etc/named/named.conf'
        'hybrid':  yes
        'dnssec-db': '{{ pdns_config_dir }}/dnssec.db'

By default this role starts just the bind-backend with an empty config file.

    pdns_mysql_databases_credentials: {}

Credentials to create the PowerDNS MySQL backend databases and users.
For example:

    pdns_mysql_databases_credentials:
      'gmysql:one':
        'priv_user': root
        'priv_password': my_first_password
        'priv_host':
          - "localhost"
          - "%"
      'gmysql:two':
        'priv_user': someprivuser
        'priv_password': my_second_password
        'priv_host':
          - "localhost"

Notice that this must only containes the credentials 
for the `gmysql` backends provided in `pdns_backends`.

    pdns_sqlite_databases_locations: []

List of the locations of the SQLite databases that have to be created if using the 
`gsqlite3` backend.

Example Playbook
----------------
Run as a master using the bind backend (when you already have a named.conf):
```
- hosts: ns1.example.net
  roles:
    - { role: PowerDNS.pdns }
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
    - { role: PowerDNS.pdns }
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
    pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"
```

Run the PowerDNS master branch from a package from repo.powerdns.com as a master
with the MySQL backend and use the root user to initialize the database and database user:
```
- hosts: ns2.example.net
  roles:
    - { role: PowerDNS.pdns }
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
    pdns_mysql_databases_credentials:
      gmysql:
        priv_user: root
        priv_password: myrootpass
        priv_host:
          - "%"
    pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"
```

Note: when using `pdns_mysql_databases_credential`, the `host`, `user`, `dbname` and `password` options become mandatory.

Run as a master on port 5300, using two different PostgreSQL databases:
```
- hosts: ns2.example.net
  roles:
    - { role: PowerDNS.pdns }
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
    - { role: PowerDNS.pdns }
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
    pdns_sqlite_databases_locations:
      - "{{ database_name }}"
```

License
-------

MIT
