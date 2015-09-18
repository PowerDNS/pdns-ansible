PowerDNS Authoritative Server
=============================

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Authoritative Server.


Requirements
------------
An Ansible installation.

Role Variables
--------------
### pdns_backends
A dict that allows you configure the backends, this also installs the correct
packages for these backends. By default, no backends are installed and PowerDNS
will be unable to start.

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
('os') or the PowerDNS repository ('PowerDNS'). This is 'os' by default.

### pdns_repo_branch
 When installing from the PowerDNS repository, what branch should be installed?
Currently only 'master' is supported.

### pdns_user
The user to run PowerDNS as, this is 'pdns' by default. This user is not (yet)
created.

### pdns_group
The group to run PowerDNS as, this is 'pdns' by default. This group is not (yet)
created.

Example Playbook
----------------
Run as a master using the bind backend:
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

Run as a slave with the MySQL backend:
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
```

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

License
-------
(C) 2015 - PowerDNS.COM BV

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Author Information
------------------
 Pieter Lexis <pieter.lexis@powerdns.com>
