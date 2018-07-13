## v1.3.0 (To be released)

NEW FEATURES:
- Allow to manage systemd overrides ([\#53](https://github.com/PowerDNS/pdns-ansible/pull/53))

IMPROVEMENTS:
- Improved documentation ([\#52](https://github.com/PowerDNS/pdns-ansible/pull/52))
- Upgrade molecule to 2.14.0 ([\#51](https://github.com/PowerDNS/pdns-ansible/pull/51))
- Improved systemd support in the tests ([\#49](https://github.com/PowerDNS/pdns-ansible/pull/49))

## v1.2.1 (2018-04-06)

BUG FIXES:
- Fix the name of the PostgreSQL backend on RHEL

## v1.2.0 (2018-04-05)

NEW FEATURES:
- Debug packages installation ([\#47](https://github.com/PowerDNS/pdns-ansible/pull/47))

IMPROVEMENTS:
- Improved test-suite ([\#47](https://github.com/PowerDNS/pdns-ansible/pull/47))
- Improved config files permissions ([\#45](https://github.com/PowerDNS/pdns-ansible/pull/45))

## v1.1.0 (2017-11-25)

IMPROVEMENTS:
- Testing across multiple ansible versions with tox ([\#43](https://github.com/PowerDNS/pdns-ansible/pull/43))

BUG FIXES:
- Fixed test cases and hardened file permissions ([\#42](https://github.com/PowerDNS/pdns-ansible/pull/42))

## v1.0.0 (2017-10-27)

IMPROVEMENTS:
- Sort configuration keys ([\#35](https://github.com/PowerDNS/pdns-ansible/pull/35), [\#37](https://github.com/PowerDNS/pdns-ansible/pull/37))

BUG FIXES:
- Fix the logic handling the different packages versions for Debian and CentOS ([\#43](https://github.com/PowerDNS/pdns-ansible/pull/43))
- Fix a few typos in the README file ([\#39](https://github.com/PowerDNS/pdns-ansible/pull/39))

## v0.1.1 (2017-10-10)

NEW FEATURES:
- Install specific PowerDNS Authoritative Server versions ([\#34](https://github.com/PowerDNS/pdns-ansible/pull/34))

IMPROVEMENTS:
- Add support to the PowerDNS Authoritative Server 4.1.x releases ([\#33](https://github.com/PowerDNS/pdns-ansible/pull/33))
- Fixing minor linter issues with whitespace ([\#30](https://github.com/PowerDNS/pdns-ansible/pull/30))

BUG FIXES:
- Fix Ubuntu APT repositories pinning ([\#32](https://github.com/PowerDNS/pdns-ansible/pull/32))

## v0.1.0 (2017-06-27)

Initial release.

NEW FEATURES:
- PostgreSQL and SQLite databases initialization
- PowerDNS Authoritative Server installation and configuration Red-Hat and Debian support
- Continuous testing with TravisCI

IMPROVEMENTS:
- Switch to the MIT License ([\#27](https://github.com/PowerDNS/pdns-ansible/pull/27))
- Overall role refactoring ([\#28](https://github.com/PowerDNS/pdns-ansible/pull/28))
