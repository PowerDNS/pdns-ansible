# Ansible Role: PowerDNS Authoritative Server

[![Build Status](https://github.com/PowerDNS/pdns-ansible/actions/workflows/main.yml/badge.svg)](https://github.com/PowerDNS/pdns-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.pdns-blue.svg)](https://galaxy.ansible.com/PowerDNS/pdns)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/pdns-ansible.svg)](https://github.com/PowerDNS/pdns-ansible/tags)

An Ansible role created by the folks behind PowerDNS to setup the [PowerDNS Authoritative Server](https://docs.powerdns.com/authoritative/).

## Requirements

An Ansible 2.9 or higher installation.

## Dependencies

None.

## Role Variables

Available variables are listed below, along with their default values (see `defaults/main.yml`):

```yaml
pdns_install_repo: ""
```

By default, the PowerDNS Authoritative Server is installed from the software repositories configured on the target hosts.

```yaml
# Install the PowerDNS Authoritative Server from the 'master' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}"

# Install the PowerDNS Authoritative Server from the '4.3.x' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_43 }}"

# Install the PowerDNS Authoritative Server from the '4.4.x' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_44 }}"
```

The examples above, show how to install the PowerDNS Authoritative Server from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

```yaml
- hosts: all
  vars:
    pdns_install_repo:
      name: "powerdns" # the name of the repository
      apt_repo_origin: "example.com"  # used to pin the PowerDNS packages to the provided repository
      apt_repo: "deb http://example.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/pdns main"
      gpg_key: "http://example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
      yum_repo_baseurl: "http://example.com/centos/$basearch/$releasever/pdns"
      yum_debug_symbols_repo_baseurl: "http://example.com/centos/$basearch/$releasever/pdns/debug"
  roles:
    - { role: PowerDNS.pdns }
```

It is also possible to install the PowerDNS Authoritative Server from custom repositories as demonstrated in the example above.
**Note:** These repositories are ignored on Arch Linux

```yaml
 pdns_install_epel: True
```

By default, install EPEL to satisfy some PowerDNS Authoritative Server dependencies like `protobuf`.
To skip the installtion of EPEL set `pdns_install_epel` to `False`.

```yaml
pdns_package_name: "{{ default_pdns_package_name }}"
```

The name of the PowerDNS Authoritative Server package, `pdns` on RedHat-like systems and `pdns-server` on Debian-like systems.

```yaml
pdns_package_version: ""
```

Optionally, allow to set a specific version of the PowerDNS Authoritative Server package to be installed.

```yaml
pdns_install_debug_symbols_package: False
```

Install the PowerDNS Authoritative Server debug symbols.

```yaml
pdns_debug_symbols_package_name: "{{ default_pdns_debug_symbols_package_name }}"
```

The name of the PowerDNS Authoritative Server debug package to be installed when `pdns_install_debug_symbols_package` is `True`,
`pdns-debuginfo` on RedHat-like systems and `pdns-server-dbg` on Debian-like systems.

```yaml
pdns_user: pdns
pdns_group: pdns
```

The user and group the PowerDNS Authoritative Server process will run as. <br />
**NOTE**: This role does not create the user or group as we assume that they've been created
by the package or other roles.

```yaml
pdns_service_name: "pdns"
```

Name of the PowerDNS service.

```yaml
pdns_service_state: "started"
pdns_service_enabled: "yes"
```

Allow to specify the desired state of the PowerDNS Authoritative Server service.

```yaml
pdns_disable_handlers: False
```

Disable automated service restart on configuration changes.

```yaml
pdns_config_dir: "{{ default_pdns_config_dir }}"
pdns_config_file: "pdns.conf"
```

PowerDNS Authoritative Server configuration file and directory.

```yaml
pdns_config: {}
```

Dictionary containing the PowerDNS Authoritative Server configuration. <br />
**NOTE:** The PowerDNS backends configuration and the `config-dir`, `setuid` and `setgid` directives must be configured through the `pdns_user`, `pdns_group` and `pdns_backends` role variables (see `templates/pdns.conf.j2`).
For example:

```yaml
pdns_config:
  master: yes
  slave: no
  local-address: '192.0.2.53'
  local-ipv6: '2001:DB8:1::53'
  local-port: '5300'
```

configures PowerDNS Authoritative Server to listen incoming DNS requests on port 5300.

```yaml
pdns_service_overrides:
  User: {{ pdns_user }}
  Group: {{ pdns_group }}
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category.

```yaml
pdns_backends:
  bind:
    config: '/dev/null'
```

Dictionary declaring all the backends you'd like to enable. You can use
multiple backends of the same kind by using the `{backend}:{instance_name}` syntax.
For example:

```yaml
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
```

By default this role starts just the bind-backend with an empty config file.

```yaml
pdns_mysql_databases_credentials: {}
```

Administrative credentials for the MySQL backend used to create the PowerDNS Authoritative Server databases and users.
For example:

```yaml
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
```

Notice that this must only contain the credentials
for the `gmysql` backends provided in `pdns_backends`.

```yaml
pdns_sqlite_databases_locations: []
```

Locations of the SQLite3 databases that have to be created if using the
`gsqlite3` backend.

```yaml
pdns_lmdb_databases_locations: []
```

Locations of the LMDB databases that have to be created if using the
`lmdb` backend.

Locations of the mysql and sqlite3 base schema.
When set, this value is used and they are not automatically detected.
```yaml
pdns_mysql_schema_file: ''

pdns_sqlite3_schema_file: ''
```

## Example Playbooks

Run as a master using the bind backend (when you already have a `named.conf` file):

```yaml
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

Install the latest '41' build of PowerDNS Authoritative Server enabling the MySQL backend.
Provides also the MySQL administrative credentials to automatically create and initialize the PowerDNS Authoritative Server user and database:

```yaml
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
```

**NOTE:** In this case the role will use the credentials provided in `pdns_mysql_databases_credentials` to automatically create and initialize the user (`user`, `password`) and database (`dbname`) connecting to the MySQL server (`host`, `port`).

Configure PowerDNS Authoritative Server in 'master' mode reading zones from two different PostgreSQL databases:

```yaml
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

Configure PowerDNS Authoritative Server to run with the `gsqlite3` backend.
The SQLite database will be created and initialized by the role
in the location specified by the `database_name` variable.

```yaml
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

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox

To test all the scenarios run

    $ tox

To run a custom molecule command

    $ tox -e ansible210 -- molecule test -s pdns-44

## License

MIT
