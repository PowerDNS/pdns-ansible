## v1.7.0 (2021-07-01)

NEW FEATURES:
- Create directory, set the ownership and permissions for LMDB databases ([\#95](https://github.com/PowerDNS/pdns-ansible/pull/95))
- Add database schema file detection on the target system with override possibility ([\#100](https://github.com/PowerDNS/pdns-ansible/pull/100))
- Add 4.4 repositories ([\#91](https://github.com/PowerDNS/pdns-ansible/pull/91))

IMPROVEMENTS:
- Use systemd task option `daemon_reload` instead of command task ([\#90](https://github.com/PowerDNS/pdns-ansible/pull/90))

REMOVED FEATURES:
- Drop EL6 support ([\#91](https://github.com/PowerDNS/pdns-ansible/pull/91), [\#94](https://github.com/PowerDNS/pdns-ansible/pull/94))
- Remove 4.1 and 4.2 repositories ([\#101](https://github.com/PowerDNS/pdns-ansible/pull/101))

BUG FIXES:
- Re-instate molecule tests ([\#100](https://github.com/PowerDNS/pdns-ansible/pull/100))

## v1.6.1 (2020-10-01)

BUG FIXES:
- Ensure install does not fail when no overrides are defined ([\#85](https://github.com/PowerDNS/pdns-ansible/pull/85))
- Ensure that `ExecStart` is overridden, not appended to ([\#86](https://github.com/PowerDNS/pdns-ansible/pull/86))

## v1.6.0 (2020-09-18)

BUG FIXES:
- Fix path to MySQL schema for Debian 10 ([\#73](https://github.com/PowerDNS/pdns-ansible/pull/73))

IMPROVEMENTS:
- Allow loading apt key from the ansible server ([\#75](https://github.com/PowerDNS/pdns-ansible/pull/75))
- CentOS 8 support ([\#74](https://github.com/PowerDNS/pdns-ansible/pull/74), [\#81](https://github.com/PowerDNS/pdns-ansible/pull/81))
- Archlinux support ([\#76](https://github.com/PowerDNS/pdns-ansible/pull/76))
- Set the ownership and permissions for config files and databases ([\#82](https://github.com/PowerDNS/pdns-ansible/pull/82))
- Ensure PowerDNS is started as an unprivileged user by default (in line with PowerDNS 4.3+ behaviour)

## v1.5.0 (2019-12-11)

BUG FIXES:
- - Fix the restart of the PowerDNS service in case of instances with different `pdns_service_name` being configured in the same play ([\#70](https://github.com/PowerDNS/pdns-ansible/pull/70))

IMPROVEMENTS:
- Add support to the PowerDNS 4.3.x release ([\#69](https://github.com/PowerDNS/pdns-ansible/pull/69))
- Add support to the PowerDNS 4.2.x release ([\#61](https://github.com/PowerDNS/pdns-ansible/pull/61))
- Install missing SQLite packages ([\#69](https://github.com/PowerDNS/pdns-ansible/pull/69))
- Improved PowerDNS configuration files and directories permissions handling ([\#69](https://github.com/PowerDNS/pdns-ansible/pull/69))
- Stop interpreting 0 & 1 as no & yes in the PowerDNS configuration template ([\#68](https://github.com/PowerDNS/pdns-ansible/pull/68))
- Fix some strings comparisons and variable types issues reported by ansible-lint ([\#66](https://github.com/PowerDNS/pdns-ansible/pull/66))
- Update the CI infrastructure to test the role against the Ansible 2.7, 2.8 and 2.9 releases ([\#67](https://github.com/PowerDNS/pdns-ansible/pull/67))
- Update the CI infrastructure to stop testing against an EOL Ubuntu release ([\#62](https://github.com/PowerDNS/pdns-ansible/pull/62))

## v1.4.0 (2018-12-02)

BUG FIXES:
- Fix handling of lists expansion in the PowerDNS configuration template ([\#55](https://github.com/PowerDNS/pdns-ansible/pull/55))

NEW FEATURES:
- Allow to disable automated restart of the service on configuration changes ([\#54](https://github.com/PowerDNS/pdns-ansible/pull/54))

## v1.3.0 (2018-07-13)

NEW FEATURES:
- Add support to systemd overrides definitions ([\#53](https://github.com/PowerDNS/pdns-ansible/pull/53))

IMPROVEMENTS:
- Implement stricter `pdns_config_dir` and `pdns_config['include-dir']` folders permissions ([\#53](https://github.com/PowerDNS/pdns-ansible/pull/53))
- Improved documentation ([\#52](https://github.com/PowerDNS/pdns-ansible/pull/52))
- Update the CI infrastructure to use molecule 2.14.0 ([\#51](https://github.com/PowerDNS/pdns-ansible/pull/51))
- Improved test coverage of systemd support ([\#49](https://github.com/PowerDNS/pdns-ansible/pull/49))

## v1.2.1 (2018-04-06)

BUG FIXES:
- Fix the name of the PostgreSQL backend on RHEL

## v1.2.0 (2018-04-05)

NEW FEATURES:
- Allow to install PowerDNS debug packages ([\#47](https://github.com/PowerDNS/pdns-ansible/pull/47))

IMPROVEMENTS:
- Improved test-suite ([\#47](https://github.com/PowerDNS/pdns-ansible/pull/47))
- Improved config files permissions handling ([\#45](https://github.com/PowerDNS/pdns-ansible/pull/45))

## v1.1.0 (2017-11-25)

IMPROVEMENTS:
- Implement testing against multiple ansible versions with tox ([\#43](https://github.com/PowerDNS/pdns-ansible/pull/43))

BUG FIXES:
- Fixed test cases and hardened file permissions ([\#42](https://github.com/PowerDNS/pdns-ansible/pull/42))

## v1.0.0 (2017-10-27)

IMPROVEMENTS:
- Implement sorting of the configuration options ([\#35](https://github.com/PowerDNS/pdns-ansible/pull/35), [\#37](https://github.com/PowerDNS/pdns-ansible/pull/37))

BUG FIXES:
- Fix the logic handling the different packages versions for Debian and CentOS ([\#43](https://github.com/PowerDNS/pdns-ansible/pull/43))
- Fix a few typos in the README file ([\#39](https://github.com/PowerDNS/pdns-ansible/pull/39))

## v0.1.1 (2017-10-10)

NEW FEATURES:
- Allow to pin the PowerDNS version to be installed ([\#34](https://github.com/PowerDNS/pdns-ansible/pull/34))

IMPROVEMENTS:
- Add support to the PowerDNS 4.1.x release ([\#33](https://github.com/PowerDNS/pdns-ansible/pull/33))
- Fixing minor linter issues with whitespace ([\#30](https://github.com/PowerDNS/pdns-ansible/pull/30))

BUG FIXES:
- Fix Ubuntu APT repositories pinning ([\#32](https://github.com/PowerDNS/pdns-ansible/pull/32))

## v0.1.0 (2017-06-27)

Initial release.

NEW FEATURES:
- MySQL and SQLite databases initialization
- PowerDNS installation and configuration with RHEL/CentOS and Debian/Ubuntu support
- Continuous testing with TravisCI

IMPROVEMENTS:
- Switch to the MIT License ([\#27](https://github.com/PowerDNS/pdns-ansible/pull/27))
- Overall role refactoring ([\#28](https://github.com/PowerDNS/pdns-ansible/pull/28))
