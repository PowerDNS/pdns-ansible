# Ansible Role: PowerDNS Authoritative Server

[![Build Status](https://github.com/PowerDNS/pdns-ansible/actions/workflows/main.yml/badge.svg)](https://github.com/PowerDNS/pdns-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.pdns-blue.svg)](https://galaxy.ansible.com/PowerDNS/pdns)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/pdns-ansible.svg)](https://github.com/PowerDNS/pdns-ansible/tags)

An Ansible role created by the folks behind PowerDNS to setup the [PowerDNS Authoritative Server](https://docs.powerdns.com/authoritative/).

## Requirements

An ansible-core 2.16 or newer installation. Enterprise Linux 8 targets must be
managed with ansible-core 2.16: their system Python is 3.6, which the modules of
ansible-core 2.20 cannot run.

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
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_master }}" }


# Install the PowerDNS Authoritative Server from the '4.8.x' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_48 }}" }

# Install the PowerDNS Authoritative Server from the '4.9.x' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_49 }}" }

# Install the PowerDNS Authoritative Server from the '5.0.x' official repository
- hosts: all
  roles:
    - { role: PowerDNS.pdns,
        pdns_install_repo: "{{ pdns_auth_powerdns_repo_50 }}" }
```

The examples above, show how to install the PowerDNS Authoritative Server from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

```yaml
- hosts: all
  vars:
    pdns_install_repo:
      name: "powerdns" # the name of the repository
      apt_repo_origin: "example.com"  # used to pin the PowerDNS packages to the provided repository
      apt_version: "auth-50"  # deb822 suites suffix (appended to release codename)
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

When `pdns_install_repo.apt_version` is set, this role configures Debian-family repositories using
`ansible.builtin.deb822_repository` on supported releases (Ubuntu `>=22.04`, Debian `>=11`).
If `apt_version` is omitted, the legacy `apt_repo` string is used with `ansible.builtin.apt_repository`.

```yaml
 pdns_install_epel: true
```

By default, install EPEL to satisfy some PowerDNS Authoritative Server dependencies like `protobuf`.
To skip the installation of EPEL set `pdns_install_epel` to `false`.

```yaml
pdns_package_name: "{{ default_pdns_package_name }}"
```

The name of the PowerDNS Authoritative Server package, `pdns` on RedHat-like systems and `pdns-server` on Debian-like systems.

```yaml
pdns_package_version: ""
```

Optionally, allow to set a specific version of the PowerDNS Authoritative Server package to be installed.

```yaml
pdns_package_state: "present"
```

Desired package state for `pdns_package_name`. Supported values include `present`, `latest`, and `absent`.
When set to `absent`, the role removes packages and skips runtime configuration tasks.

```yaml
pdns_install_debug_symbols_package: false
```

Install the PowerDNS Authoritative Server debug symbols.

```yaml
pdns_debug_symbols_package_name: "{{ default_pdns_debug_symbols_package_name }}"
```

The name of the PowerDNS Authoritative Server debug package to be installed when `pdns_install_debug_symbols_package` is `true`,
`pdns-debuginfo` on RedHat-like systems and `pdns-server-dbg` on Debian-like systems.

```yaml
pdns_debug_symbols_package_state: "{{ pdns_package_state }}"
```

Desired package state for the debug symbols package when it is managed by this role.

```yaml
pdns_user: pdns
pdns_group: pdns
pdns_file_owner: root
pdns_file_group: "{{ pdns_group }}"
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
pdns_service_enabled: true
pdns_service_masked: false
```

Allow to specify the desired state of the PowerDNS Authoritative Server service.

```yaml
pdns_disable_handlers: false
```

Disable automated service restart on configuration changes.

```yaml
pdns_flush_handlers: false
```

Run the notified handlers at the end of the role instead of at the end of the play. See
[Handlers](#handlers).

```yaml
pdns_manage_selinux: true
```

Enable management of SELinux booleans and ports on SELinux-enabled systems.
Set to `false` to skip SELinux changes entirely.

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
  primary: true
  secondary: false
  local-address: '192.0.2.53'
  local-ipv6: '2001:DB8:1::53'
  local-port: '5300'
```

configures PowerDNS Authoritative Server to listen incoming DNS requests on port 5300.

```yaml
pdns_service_overrides:
  User: "{{ pdns_user }}"
  Group: "{{ pdns_group }}"
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category.
The role writes them to `/etc/systemd/system/<service name>.service.d/override.conf`. Setting
`pdns_service_overrides: {}` removes that file again and restarts the service on the packaged
unit, so the `User` and `Group` of the default above go back to the values of the package. Other
drop-ins in the same directory are left alone.

```yaml
pdns_backends_packages: "{{ default_pdns_backends_packages }}"
pdns_backends_packages_state: "{{ pdns_package_state }}"
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
    'hybrid': true
    'dnssec-db': '{{ pdns_config_dir }}/dnssec.db'
```

By default this role starts just the bind-backend with an empty config file.
`pdns_backends_packages_state` controls install/update/removal of backend packages.

```yaml
pdns_config_additional_dirs: []
```

Optional list of directories created before `pdns_config_files` are copied.
Each item can be either a path string or an object with `path`, `owner`, `group`, `mode`.
For example:

```yaml
pdns_config_additional_dirs:
  - path: "{{ pdns_config['include-dir'] }}"
    mode: "0775"
  - "{{ pdns_config_dir }}/zones"
  - "/var/lib/powerdns/rpz"
```

```yaml
pdns_config_files: []
```

Optional list of files copied before the service is started.
Each item must define `dest` and one of `src` or `content`.
`dest` can be absolute or relative to `pdns_config_dir`.
Executable backend helper scripts should be shipped via this variable too
(for example with `mode: "0750"`).
For example:

```yaml
pdns_config_files:
  - src: files/pdns/named.conf
    dest: named.conf
    mode: "0640"
  - dest: pipe-backend.py
    mode: "0750"
    content: |
      #!/usr/bin/env python3
      print("example")
```

```yaml
pdns_mysql_manage_database: true
pdns_mysql_flavor: mysql
pdns_mysql_databases_credentials: {}
pdns_mysql_query_use_socket: false
pdns_mysql_unix_socket: "/var/run/mysqld/mysqld.sock"
pdns_backends_mysql_cmd: "{{ default_pdns_backends_mysql_cmd }}"
pdns_mysql_cli_extra_args: "{{ default_pdns_mysql_cli_extra_args }}"
pdns_mysql_auth_plugin: ""
pdns_mysql_user_update_password: ""
pdns_mysql_packages: "{{ default_pdns_mysql_packages }}"
pdns_mysql_packages_state: "present"
```

`pdns_mysql_manage_database` controls whether this role performs MySQL/MariaDB bootstrap operations
(database creation, user/grants management and schema checks/import).
Set it to `false` for config-only mode.

`pdns_mysql_flavor` selects which collection creates the database and the user of
the `gmysql` backend: `ansible.mysql` for the default `mysql`, `ansible.mariadb`
for `mariadb`. The two are one code base split in two. `ansible.mysql` still
manages a MariaDB server and only warns that its support ends in 6.0.0, so the
default works for both servers and nothing changes for an existing playbook. Set
`mariadb` to move a MariaDB server to the collection that keeps supporting it;
the settings written to `pdns.conf`, the client packages and the schema import
are identical either way.

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

When `pdns_mysql_query_use_socket` is set to `true`, role-internal MySQL operations
(database/user creation and schema load checks/import) use the UNIX socket path defined by
`pdns_mysql_unix_socket` instead of TCP host/port.
`pdns_backends_mysql_cmd` and `pdns_mysql_cli_extra_args` control the MySQL/MariaDB CLI invocation used for schema checks/import.
`pdns_mysql_packages` allows overriding OS-specific MySQL dependency package lists.
`pdns_mysql_packages_state` controls install/update/removal of those dependency packages.

```yaml
pdns_pgsql_manage_database: true
pdns_pgsql_databases_credentials: {}
pdns_pgsql_packages: "{{ default_pdns_pgsql_packages }}"
pdns_pgsql_packages_state: "present"
```

`pdns_pgsql_manage_database` controls whether this role performs PostgreSQL bootstrap operations
(database/user creation and schema checks/import).
Set it to `false` for config-only mode.

Administrative credentials for the PostgreSQL backend used to create the PowerDNS Authoritative Server databases and users.
For example:

```yaml
pdns_pgsql_databases_credentials:
  'gpgsql:one':
    priv_user: postgres
    priv_password: my_first_password
```

Notice that this must only contain the credentials
for the `gpgsql` backends provided in `pdns_backends`.

```yaml
pdns_pgsql_query_use_socket: false
pdns_pgsql_unix_socket: "/var/run/postgresql"
```

When `pdns_pgsql_query_use_socket` is set to `true`, role-internal PostgreSQL operations
(database/user creation and schema load checks/import) use the UNIX socket path defined by
`pdns_pgsql_unix_socket` instead of TCP host/port.
`pdns_pgsql_packages` allows overriding OS-specific PostgreSQL dependency package lists.
`pdns_pgsql_packages_state` controls install/update/removal of those dependency packages.

```yaml
pdns_sqlite_databases_locations: []
```

Locations of the SQLite3 databases that have to be created if using the
`gsqlite3` backend.

```yaml
pdns_sqlite_package_state: "present"
```

Desired package state for the SQLite CLI dependency used during schema bootstrap.

```yaml
pdns_lmdb_databases_locations: []
```

Locations of the LMDB databases that have to be created if using the
`lmdb` backend.

Locations of the mysql, pgsql and sqlite3 base schema.
When set, this value is used and they are not automatically detected.
```yaml
pdns_mysql_schema_load: true
pdns_mysql_schema_file: ''
pdns_mysql_schema_on_first_node_only: true

pdns_pgsql_schema_load: true
pdns_pgsql_schema_file: ''
pdns_pgsql_schema_on_first_node_only: true

pdns_sqlite_schema_file: ''
```

`pdns_mysql_schema_load` and `pdns_pgsql_schema_load` only control schema check/import tasks.
When SQL bootstrap is enabled (`pdns_mysql_manage_database` / `pdns_pgsql_manage_database`) and
administrative credentials are provided, user/database creation still runs even if schema load is disabled.

`pdns_mysql_schema_on_first_node_only` and `pdns_pgsql_schema_on_first_node_only` control
cluster bootstrap execution for shared SQL backends (database/user/grants/schema import).

```yaml
pdns_verbose: "{{ ansible_verbosity | int >= 2 }}"
```

Enable verbose/debug role behavior. This currently controls whether sensitive SQL task details
are hidden in logs (`false`) or visible for troubleshooting (`true`).

## Role Tags

Tags for `--tags` / `--skip-tags`:

- `repository`: repo and GPG key setup, pinning, cache refresh.
- `install`: package installation and removal.
- `config`: templates, files, directories, settings, data bootstrap.
- `service`: service state and related handlers.
- `backend`: database backend management, all backends. No per-backend tags.
- `selinux`: SELinux policy tasks.
- `always`: OS variable import.

Prerequisites carry several tags. The fact deriving the repository name is tagged `install` +
`repository`; version detection is tagged `config` + `backend`, since the backend tasks need the
running version to locate the schema files.

Contributors: tags belong on the tasks inside the included files, not only on the `include_tasks`
in `tasks/main.yml`. A dynamic `include_tasks` does not pass its tags to included tasks, so a task
relying on the include's tag alone is skipped by a narrow `--tags` run - silently, or with an
undefined-variable error in whatever depended on it.

## Check Mode

Supported only on a host where this role already ran successfully.

Converged host: `--check` reports real drift only. The read-only probes locating schema files and
the running version carry `check_mode: false` so they still run and register results; they change
nothing. Without that, check mode reasons about schema state from empty strings.

Fresh host: `--check` is expected to fail. It installs neither the repository, `python3-debian` nor
the `pdns` packages, so the run aborts in `deb822_repository` or on the
`Ensure PowerDNS version was detected` assertion.

`Check if the PostgreSQL databases are empty` uses `community.postgresql.postgresql_query`, which
honours check mode natively but needs a reachable database.

## Package and Service State

- `pdns_package_state`: `present`, `latest`, `absent`, ...
- `pdns_debug_symbols_package_state`, `pdns_backends_packages_state`, `pdns_mysql_packages_state`,
  `pdns_pgsql_packages_state`, `pdns_sqlite_package_state`: default to `pdns_package_state`.
- `pdns_service_state` (`started`, `stopped`, `restarted`, `reloaded`), `pdns_service_enabled`,
  `pdns_service_masked`.

Removal works in a normal run: with `pdns_package_state: absent` the packages are removed and the
version detection, SELinux, backend, config, service and provisioning stages are skipped.

```bash
ansible-playbook site.yml -e pdns_package_state=absent
```

## Handlers

Handlers run at the end of the play, and Ansible shares them between invocations of the same role.
A role parameter read inside a handler resolves to the value of the *last* invocation, so with more
than one invocation in a play the restart targets the wrong service or is collapsed into a single
run. Set `pdns_flush_handlers: true` to run `meta: flush_handlers` as the last task of the role,
which restarts `pdns_service_name` of that invocation:

Every instance needs its own service name and configuration file; `pdns@<instance>` runs
`pdns_server --config-name=<instance>`, which reads `<config dir>/pdns-<instance>.conf`:

```yaml
- hosts: ns1.example.net
  tasks:
    - name: Authoritative server 'a'
      ansible.builtin.include_role:
        name: PowerDNS.pdns
      vars:
        pdns_service_name: pdns@a
        pdns_config_file: pdns-a.conf
        pdns_flush_handlers: true
        pdns_config:
          local-port: "5401"

    - name: Authoritative server 'b'
      ansible.builtin.include_role:
        name: PowerDNS.pdns
      vars:
        pdns_service_name: pdns@b
        pdns_config_file: pdns-b.conf
        pdns_flush_handlers: true
        pdns_config:
          local-port: "5402"
```

`meta: flush_handlers` is play-wide: it also runs handlers that earlier roles in the same play
notified. `pdns_disable_handlers: true` skips the restart handlers entirely.

`pdns_flush_handlers` defaults to `false`, which is correct for a single invocation and wrong for
more than one: without it the pending restarts of every instance run once, at the end of the play,
against the service name of the last invocation.

The restart handler reloads the systemd units in the same task, so a restart never runs against a
unit systemd has not read. The reload happens even when `pdns_service_state: stopped` keeps the
service down, so the next manual start uses the drop-in this run wrote.

Ansible does not filter handlers by tag, so the restart handler reads `ansible_skip_tags` itself:
under `--skip-tags service` the service task is skipped and the handler restarts nothing, while
the systemd units of that run are still reloaded. `--tags config` is unaffected and still restarts.
`pdns_disable_handlers: true` remains the way to apply configuration without restarting in a run
that is not tag-filtered.

With `pdns_provision: true` the role always flushes the handlers before provisioning, whatever
`pdns_flush_handlers` is set to: provisioning talks to the API of the running server at the
configured address, port and API key, so it fails against a server that has not picked up the new
configuration yet. A configuration change left unapplied by an earlier run cannot be detected, since
nothing notifies the handler in the next run; restart the service manually in that case.

## Provisioning

With `pdns_provision: true` the role provisions data through the REST API of the
instance it just configured. Each resource has its own list:

| Variable | Resource |
|----------|----------|
| `pdns_provision_autoprimaries` | Autoprimaries |
| `pdns_provision_zones` | Zones, including catalog zones |
| `pdns_provision_records` | Records of a zone, one entry per RRset |
| `pdns_provision_zone_metadata` | Metadata of a zone |
| `pdns_provision_cryptokeys` | DNSSEC keys of a zone |
| `pdns_provision_tsigkeys` | TSIG keys |
| `pdns_provision_views` | Zones of a view |
| `pdns_provision_networks` | Networks mapped to a view |
| `pdns_provision_pdnsutils` | Commands run through `pdnsutil` |

> **`pdns_autoprimaries` is deprecated and will be removed in the next release.**
> Rename it to `pdns_provision_autoprimaries`, which is the same list under the
> name the rest of the family uses. Nothing breaks in the meantime:
> `pdns_provision_autoprimaries` defaults to `pdns_autoprimaries`, so a playbook
> that still sets the old name keeps working, and setting the new name takes
> precedence over the old one.

**Every entry is submitted to the API as written.** The role does not interpret,
rename or reorder the fields, so a field the API accepts works whether or not the
role knows about it - the reference is
[the API documentation](https://doc.powerdns.com/authoritative/http-api/), not
this README. Only a few keys per list are read by the role itself, to build the
request URL, and they are removed from the body before it is sent: `name` for a
zone or a TSIG key, `zone` for a record, `zone` and `kind` for metadata, `zone` and `force` for a
DNSSEC key, `view` and `zones` for a view, `network` for a network, and `ip` and
`nameserver` for an autoprimary.

**Provisioning adds and removes nothing.** An entry that is already there is left
alone, and anything on the server that no list mentions is left alone as well.

```yaml
- hosts: all
  roles:
    - role: PowerDNS.pdns
      pdns_provision: true
      pdns_provision_zones:
        - name: catalog.invalid.
          kind: Producer
        - name: example.com.
          kind: Native
          catalog: catalog.invalid.
          nameservers:
            - ns1.example.com.
      pdns_provision_zone_metadata:
        - zone: example.com.
          kind: ALLOW-AXFR-FROM
          metadata:
            - 127.0.0.0/8
      pdns_provision_cryptokeys:
        - zone: example.com.
          keytype: csk
          algorithm: ECDSAP256SHA256
          active: true
      pdns_provision_tsigkeys:
        - name: axfr-key
          algorithm: hmac-sha256
```

A **catalog zone** is an ordinary zone with `kind` set to `Producer` or
`Consumer`, and a member joins one by naming it in `catalog`, so both are
declared in `pdns_provision_zones`.

### Records

A zone and its records are separate resources with separate endpoints, so they are
declared separately. `pdns_provision_zones` brings the zone into existence;
`pdns_provision_records` brings its records to the declared state. Records written
inside a `pdns_provision_zones` entry only apply when that zone is *created*,
because the create is the one request that carries them - after that the zone
endpoint deals in attributes alone.

```yaml
pdns_provision_records:
  - zone: example.com.
    name: www.example.com.
    type: A
    ttl: 3600
    records:
      - content: 192.0.2.1
      - content: 192.0.2.2
  - zone: example.com.
    name: retired.example.com.
    type: A
    changetype: DELETE
```

Each entry is one RRset. `changetype` defaults to `REPLACE`, which creates the
RRset or replaces it wholesale; it is scoped to one name and type and leaves every
other record in the zone alone. `DELETE` removes it and needs only `name` and
`type`. That pair is the whole cycle - create, update and delete - and both verbs
are safe to repeat.

There is no prune for records. An RRset the list does not mention is left alone,
and `DELETE` is how one is taken away, because "remove every record I did not
declare" would empty a zone the moment a list was incomplete.

A trailing dot is added to `name` when it is missing, so `www.example.com` and
`www.example.com.` both work.

Each entry is compared against the zone as it stands before anything is written,
so an entry that already matches is not sent. That keeps a repeated converge at
`changed=0`, and it keeps the zone's SOA serial still: the serial moves on every
PATCH the API receives, including one that changes nothing.

**Views** need `views: yes` in `pdns_config`. A member of a view is a zone named
`<zone>..<variant>` and has to be declared in `pdns_provision_zones` before it
can join, because it has to exist as a zone first.

### Repeating a run

Each list is compared against what the API reports before anything is written, so
a second converge reports no change. Two resources need more care:

**DNSSEC keys cannot be matched.** Creating one answers 201 every time and
returns a newly generated key, and the API exposes nothing that would let a later
run recognise a key this role created - so posting the same entry twice simply
leaves the zone with two different keys. An entry is therefore only created while
its zone has no keys at all, and a zone that already has keys is left untouched.
Set `force: true` on an entry to post it regardless, which is what a key rollover
needs; an entry left on `force` writes a new key on every run, so it belongs in a
one-off run rather than in inventory.

A consequence worth knowing: if one entry of a batch is created and a later one
fails, or the run is interrupted between them, the next converge finds the zone
already carrying keys and skips the rest **silently**. The zone is left with fewer
keys than declared and nothing says so. The same guard is why "add a second key to
a zone that already has one" needs `force: true`.

**Metadata is written with PUT**, which replaces the values of one kind and leaves
every other kind of the zone alone. An entry declaring `metadata: []` removes
that kind, which is how metadata is taken away - there is no prune for it.

**Give names and networks in the form the API stores them.** Each list is compared
against what the API returns, and the API canonicalizes: a zone name needs its
trailing dot (`example.com.`, not `example.com` - the API rejects the latter with
`DNS Name is not canonical`), and a network needs its network address rather than
a host address inside it (`192.0.2.0/24`, not `192.0.2.1/24`). A network given in
non-canonical form is stored under its canonical name, so the comparison never
matches it: the mapping is rewritten on every converge, and with
`pdns_provision_prune` enabled the prune then unmaps what the same run just
mapped. Zone `kind` and a TSIG key's trailing dot are normalized by the role
itself and need no care.

### pdnsutil

For what the REST API cannot do - a backend with no API support, a subcommand with
no API equivalent, a bulk edit - `pdns_provision_pdnsutils` runs commands through
`pdnsutil`:

```yaml
pdns_provision_pdnsutils:
  - args: create-zone example.com ns1.example.com
    unless: list-zone example.com
  - args: secure-zone example.com
    unless: show-zone example.com
```

`args` is the pdnsutil arguments without the binary. `unless` is optional and is
the arguments of a probe that succeeds when the work is already done; the command
runs only when the probe fails. pdnsutil subcommands are not idempotent by
themselves - `create-zone` on an existing zone fails - so `unless` is what makes an
entry safe to repeat. **An entry without `unless` runs on every converge and
reports changed every time**, so give one to anything that should settle.

**The commands run as `pdns_user`, never as root.** pdnsutil writes the backend's
own files directly - the LMDB database, the SQLite file, the BIND zone files - and
run as root it leaves them owned by root, after which the unprivileged server can
no longer write them. That damage outlives the converge and running the role again
does not repair it. `become_user` also gives the command the groups that account is
in, which is the set the daemon gets from its unit's `User=`; a unit with a `Group=`
outside them has to pass it in through `pdns_provision_pdnsutils_command`.

```yaml
pdns_provision_pdnsutils_command: >-
  pdnsutil --config-dir={{ pdns_config_dir }} [--config-name=<instance>]
```

The invocation the arguments are appended to. It carries the configuration
directory, and for an instance whose configuration file is `pdns-<name>.conf` the
`--config-name` that selects it - pdnsutil addresses one instance at a time and
works on the default one otherwise, which is silent until the data is in the wrong
database. Override it to reach a pdnsutil that is not on `PATH` or to add flags.

### Zones that do not exist yet

Metadata and DNSSEC keys are addressed under a zone, and the API answers 404 when
that zone is absent. With `pdns_provision_ignore_missing_zone: true`, the default,
such an entry is skipped instead of failing the play, which is what a zone created
by something other than this role needs. Set it to `false` to have a missing zone
fail the run.

### Changing and removing data

```yaml
pdns_provision_update_existing: false
pdns_provision_prune: false
```

`pdns_provision_update_existing` writes the declared attributes of a zone entry -
`kind`, `catalog`, `masters`, `account` and the rest - onto a zone that already
exists. Records are not touched: a PUT on a zone carries attributes only.

`pdns_provision_prune` deletes what the lists do not declare: autoprimaries, TSIG
keys and view members, and it unmaps a network from its view. Zones and DNSSEC
keys are never deleted whatever it is set to, because dropping a zone or a key is
not a decision a converge should take.

**A prune only removes entries alongside the ones its own list declares.** A list
that is empty prunes nothing, so emptying a list does not remove the last entry -
delete that one by hand. The reason is that this role is written to be included
more than once in a play, one invocation per instance: an empty list means "this
invocation has nothing to say about these", and reading it as "delete them all"
would have the invocation that declares no TSIG keys delete the keys the previous
one just created, on every converge. View membership is likewise pruned only
within the views `pdns_provision_views` names.

### Clusters

```yaml
pdns_provision_run_once: false
```

Provisioning writes into the storage backend through the API of one instance, so
where several hosts share one database - `gmysql`, `gpgsql`, or `gsqlite3` on
shared storage - a play over the cluster otherwise repeats every request once per
host. `pdns_provision_run_once: true` runs it against the first host of the play
only.

It is off by default because it is only correct when the backend really is
shared. With a per-host backend - `lmdb`, `bind`, or a local `gsqlite3` file -
each host has a database of its own, and running once would leave every host but
the first unprovisioned.

### Check mode

Provisioning is skipped under `ansible-playbook --check`. `ansible.builtin.uri`
has no check mode of its own and fails outright, and there is nothing to simulate
either, since provisioning talks to a running instance.

## Example Playbooks

Run as a primary using the bind backend (when you already have a `named.conf` file):

```yaml
- hosts: ns1.example.net
  roles:
    - { role: PowerDNS.pdns }
  vars:
    pdns_config:
      primary: true
      local-address: '192.0.2.53'
    pdns_backends:
      bind:
        config: '/etc/named/named.conf'
```

Install the latest '50' build of PowerDNS Authoritative Server enabling the MySQL backend.
Provides also the MySQL administrative credentials to automatically create and initialize the PowerDNS Authoritative Server user and database:

```yaml
- hosts: ns2.example.net
  roles:
    - { role: PowerDNS.pdns }
  vars:
    pdns_config:
      primary: true
      secondary: false
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
    pdns_install_repo: "{{ pdns_auth_powerdns_repo_50 }}"
```

**NOTE:** In this case the role will use the credentials provided in `pdns_mysql_databases_credentials` to automatically create and initialize the user (`user`, `password`) and database (`dbname`) connecting to the MySQL server (`host`, `port`).

Configure PowerDNS Authoritative Server in 'primary' mode reading zones from two different PostgreSQL databases:

```yaml
- hosts: ns2.example.net
  roles:
    - { role: PowerDNS.pdns }
  vars:
    pdns_config:
      primary: true
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
    database_name: '/var/lib/powerdns/pdns.sqlite3'
    pdns_config:
      primary: true
      secondary: false
      local-address: '192.0.2.73'
    pdns_backends:
      gsqlite3:
        database: "{{ database_name }}"
        dnssec: true
    pdns_sqlite_databases_locations:
      - "{{ database_name }}"
```

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox
    $ tox

See [molecule/README.md](./molecule/README.md) for the test layout, how to run a
single leg, which storage backends the backend matrix covers, and what to change
when a new release, operating system or backend has to be covered.

## License

MIT
