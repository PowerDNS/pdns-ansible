PowerDNS Authoritative DNS Server Role
======================================

[![Build Status](https://travis-ci.org/PowerDNS/pdns-ansible.svg?branch=master)](https://travis-ci.org/PowerDNS/pdns-ansible)

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Authoritative Server.

Requirements
------------

An Ansible 2.0 or higher installation.

Role Variables
--------------

Available variables are listed below, along with their default values (see `defaults/main.yml`):

    pdns_install_repo: ""

By default, no PowerDNS repository will be configured by this role.
You can install the PowerDNS packages from the official PowerDNS 
repository overriding the `pdns_install_repo` variable as follows:

    # Install PowerDNS from the 'master' official repository
    - hosts: all
      roles:
        - { role: PowerDNS.pdns,
            pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"

    # Install PowerDNS from the '4.0.x' official repository
    - hosts: all
      roles:
        - { role: PowerDNS.pdns,
            pdns_install_repo: "{{ pdns_auth_powerdns_repo_40 }}"

    # Install PowerDNS from the '4.1.x' official repository
    - hosts: all
      roles:
        - { role: PowerDNS.pdns,
            pdns_install_repo: "{{ pdns_auth_powerdns_repo_41 }}"

The completed lists of the available pre-configured repositories is available in the `vars/main.yml` file.

To install PowerDNS from a custom repositories follow the instructions below

    - hosts: all
      vars:
        pdns_install_repo:
          apt_repo_origin: "my.repo.com"  # Pin the PowerDNS packages to the provided repository origin
          apt_repo: "deb http://my.repo.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/pdns main"
          gpg_key: "http://my.repo.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
          gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
          yum_repo_baseurl: "http://my.repo.com/centos/$basearch/$releasever/pdns"
          name: "powerdns"       # the name of the repository 
      roles:
        - { role: PowerDNS.pdns }

Note that not all the keys of the `pdns_install_repo` dictionary are required. i.e., if the target hosts are running on Debian it's not necessary to provide the yum repository information.

    pdns_install_epel: True

On RedHat-like system, this role configures EPEL by default.
EPEL is needed to satisfy some PowerDNS dependencies like `protobuf`.
To skip EPEL installation set `pdns_install_epel` to `False`.

    pdns_package_name: "{{ default_pdns_package_name }}"

The name of the PowerDNS package, `pdns` on RedHat-like systems and `pdns-server` on Debian-like systems.

    pdns_package_version: ""

The version of the PowerDNS package to be installed. <br />
**NOTE:** The usage of this variable makes only sense on RedHat-like systems, where each YUM repository can contains multiple versions of the same package.
For that reason, we highly recommend to not override the default value on Debian.

    pdns_user: pdns
    pdns_group: pdns

The user and group the PowerDNS process will run as.
**NOTE**: This role does not create the user or group as we assume that they've been created
by the package or other roles.

    pdns_service_name: "pdns"

Name of the PowerDNS service.

    pdns_flush_handlers: False

Force the execution of the handlers at the end of the role. <br />
**NOTE:** This is required if using this role to configure multiple PowerDNS instances in the same play.
See PowerDNS virtual hosting https://doc.powerdns.com/md/authoritative/running/#starting-virtual-instances-with-system.

    pdns_config_dir: "{{ default_pdns_config_dir }}"
    pdns_config_file: "pdns.conf"

PowerDNS configuration file and directory.

    pdns_config: {}

A dict containing the PowerDNS configuration. <br />
**NOTE:** The PowerDNS backends configuration and the `config-dir`, `setuid` and `setgid` directives must be configured through the `pdns_user`, `pdns_group` and `pdns_backends` role variables (see `templates/pdns.conf.j2`).
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

A dict with all the backends you'd like to enable. You can use
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

Administrative credentials for the MySQL backend used to create the PowerDNS databases and users.
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

Locations of the SQLite3 databases that have to be created if using the 
`gsqlite3` backend.

Example Playbooks
-----------------

Run as a master using the bind backend (when you already have a `named.conf` file):

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


Install the latest 'master' build of PowerDNS and enable the MySQL backend:

    - hosts: ns2.example.net
      roles:
        - { role: PowerDNS.pdns }
      vars:
        pdns_config:
          master: true
          local-address: '192.0.2.54'
        pdns_backends:
          gmysql:
            host: 192.0.2.120
            port: 3306
            user: powerdns
            password: P0w3rDn5
            dbname: pdns
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"


Install the latest '41' build of PowerDNS enabling the MySQL backend.
Provides also the MySQL administrative credentials to automatically create and initialize the PowerDNS user and database:

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
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_41 }}"

**NOTE:** In this case the role will use the credentials provided in `pdns_mysql_databases_credentials` to automatically create and initialize the user (`user`, `password`) and database (`dbname`) connecting to the MySQL server (`host`, `port`).


Configure PowerDNS in 'master' mode reading zones from two different PostgreSQL databases:

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


Configure PowerDNS to run with the gsqlite3 backend.
The SQLite database will be created and initialized by the role
in the location specified by the `database_name` variable.

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

License
-------

MIT
