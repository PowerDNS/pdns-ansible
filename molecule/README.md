# Molecule test layout

```
molecule/config.yml        shared driver, provisioner and verifier configuration
molecule/platforms/*.yml   platform sets, one per group of operating systems
molecule/default/         install from a PowerDNS repository, one instance per backend
molecule/multi-instance/  two instances of pdns@.service in a single play
molecule/os-repos/        install from the packages of the distribution
molecule/resources/       playbooks, task files, variables and tests shared by all
```

Three things vary independently and none of them is a scenario:

- the **release** under test, taken from `PDNS_AUTH_VERSION` (`49`, `50`, `51`),
- the **platforms**, taken from the platform set passed with `--base-config`,
- the **ansible-core version**, which follows the platforms and is never chosen
  separately. Enterprise Linux 8 has Python 3.6, which only ansible-core 2.16 can
  manage, and Ubuntu 20.04 has 3.8; everything else runs 2.20, plus one 2.18 leg
  to keep the templating engine from before the 2.19 rewrite covered. See
  [Ansible legs](#ansible-legs).

Run one leg like this:

```bash
PDNS_AUTH_VERSION=51 tox -e ansible220 -- molecule \
  -c molecule/config.yml \
  -c molecule/platforms/pdns-51.yml \
  test -s default
```

`default` and `os-repos` share their whole body: both import
`molecule/resources/converge-backends.yml`, which configures one instance per
storage backend (LMDB, SQLite, MySQL, MariaDB, Bind, PostgreSQL) plus the masked
default service. The only difference is which `vars/pdns-repo-<scenario>.yml` the
plays load, selected by `MOLECULE_SCENARIO_NAME`.

The MySQL, MariaDB and PostgreSQL servers are sibling containers defined once in
`molecule/resources/vars/services.yml`. `create.yml` starts them only when
`MOLECULE_WITH_SERVICES` is set, which `default` and `os-repos` do in their
`molecule.yml`, so `multi-instance` does not pay for booting them.

A bare `molecule` command does not pick this configuration up - Molecule only
auto-discovers a base config at `.config/molecule/config.yml`. Always pass
`-c molecule/config.yml`, which `tox` does for you.

## Containers and privileges

`molecule/resources/create.yml` builds and starts the containers from the
`Dockerfile.*.j2` templates next to it, one per init system family, and runs
systemd as PID 1 so the role manages real units.

Every image creates an unprivileged `ansible` account with passwordless sudo.
`molecule/config.yml` connects as that account and escalates from it, so the
tests take the same path a deployment does, and a task only names `become_user`
when it needs a service account, which here is the `pdnsutil` calls of
`molecule/resources/tasks/pdns-zone.yml`.

The Enterprise Linux template adds one line to `/etc/pam.d/sudo`:

```
account    sufficient   pam_localuser.so
```

Without it the account phase of `pam_unix` cannot retrieve the shadow data of
the local accounts of these images on some hosts, and it aborts every escalation
with `PAM account management error: Authentication service cannot retrieve
authentication info`. Only the account phase of sudo is short-circuited:
authentication, the shared `system-auth` stack and the sudoers policy are
untouched, and accounts that do not exist locally are still rejected.

## Ansible legs

Three ansible-core versions are tested. Which one applies follows from the
platform set, never from the scenario:

| leg | tox env | target Python floor | what it is for |
|---|---|---|---|
| 2.16 | `ansible216` | 3.6 | Enterprise Linux 8, and Ubuntu 20.04 where the release has focal packages. 2.16 is the last ansible-core whose modules run on Python 3.6 and those hosts cannot move to a newer one, so the role has to keep working with it. These platforms never run under another leg. |
| 2.18 | `ansible218` | 3.8 | The last release before the 2.19 templating rewrite, run on **one** platform of the newest release. Enterprise Linux 8 cannot serve this purpose because its Python 3.6 is below the 3.8 floor of 2.18. |
| 2.20 | `ansible220` | 3.9 | Current. Every platform except Enterprise Linux 8 and Ubuntu 20.04. |

## Platform sets

Every release has its own pair of sets, so a set lists exactly the operating
systems upstream publishes packages for. Nothing has to be inferred from a
generic name:

| set | contents | leg |
|---|---|---|
| `pdns-<newest>` | every operating system that release has packages for, from Enterprise Linux 9 upwards | `ansible220` |
| `pdns-<older>` | one RPM host and one DEB host of that release | `ansible220` |
| `pdns-<release>-ansible216` | Enterprise Linux 8 always, and Ubuntu 20.04 where that release has focal packages | `ansible216` only |
| `pdns-<newest>-ansible218` | one platform | `ansible218` only |
| `pdns-<newest>-ansible216-single` | one Enterprise Linux 8 host | `ansible216`, `multi-instance` only |

The 2.16 split exists because of the target Python, not preference: Enterprise
Linux 8 has 3.6 and Ubuntu 20.04 has 3.8. Those platforms are **never** run with
`ansible218` or `ansible220`.

The narrow sets exist because every CI job builds its own images - the runners
start with an empty image store - so each platform in a set costs an image build
and a converge of every storage backend in every run. Only the newest release
therefore carries the full operating system matrix: what changes between releases
is the upstream repository path and which packages exist for it, which one RPM
host and one DEB host establish, while the role logic that varies per operating
system is covered by the newest release's set. For the same reason the
`ansible218` leg runs on one platform, since templating does not vary per
operating system, and the `multi-instance` 2.16 leg runs on one Enterprise Linux 8
host, since what it can break is ansible-core version specific rather than vendor
specific.

Every platform that this trades away is **commented out in the set itself**, with
the reason, so widening coverage again is a matter of uncommenting.

Availability is sparse, which is exactly why the sets are per release. Upstream
publishes Enterprise Linux 10 and Debian 13 only from the second-newest release
onwards, Ubuntu 26.04 only for the newest, and focal only for `pdns-49`.
AlmaLinux is not tested because it tracks Rocky; Oracle is kept because it
diverges.

## Adding a new release, for example Authoritative Server 5.2

Upstream names its repositories `auth-52`, so `52` is the value used everywhere
below. Availability is sparse and a missing repository fails a whole
leg, so step 3 checks every operating system before the sets are written.

1. **`vars/main.yml`** - add a `pdns_auth_powerdns_repo_52` block. Copy the newest
   existing one and change every occurrence of the release number. Confirm the
   signing key is still the same as the previous release; PowerDNS has used more
   than one.
2. **`defaults/main.yml`** - add the commented usage example for the new preset,
   next to the others.
3. **Four new platform sets.** Check availability first, then list exactly what
   exists:

   ```bash
   for os in 8 9 10; do curl -sI https://repo.powerdns.com/el/x86_64/$os/auth-52/repodata/repomd.xml | head -1; done
   for s in bullseye bookworm trixie focal jammy noble resolute; do
     curl -sI https://repo.powerdns.com/{debian,ubuntu}/dists/$s-auth-52/Release 2>/dev/null | head -1
   done
   ```

   - `molecule/platforms/pdns-52.yml` - the full operating system matrix, which only
     the newest release carries: Enterprise Linux 9 upwards, Debian and Ubuntu 22.04
     upwards. Copy the set of the release that was newest until now, uncomment the
     platforms it had narrowed away, and delete what has no packages. Keep
     `groups: ["pdns"]` on every platform: the plays and the verifier target that
     group.
   - `molecule/platforms/pdns-52-ansible216.yml` - Enterprise Linux 8, plus
     Ubuntu 20.04 only if `focal-auth-52` exists.
   - `molecule/platforms/pdns-52-ansible218.yml` - one platform, Debian 13.
   - `molecule/platforms/pdns-52-ansible216-single.yml` - one Enterprise Linux 8
     host.

4. **Narrow the release that was newest until now.** In `pdns-51.yml`, comment out
   every platform except one RPM host and one DEB host, keeping the reason in the
   file, and delete `pdns-51-ansible218.yml` and `pdns-51-ansible216-single.yml`:
   those two only ever apply to the newest release.
5. **`.github/workflows/main.yml`** - add one row per set:

   ```yaml
   - {scenario: default, version: "52", platforms: pdns-52-ansible216, toxenv: ansible216}
   - {scenario: default, version: "52", platforms: pdns-52, toxenv: ansible220}
   ```

   Repoint the single `ansible218` row at `pdns-52-ansible218`.

6. **Move `multi-instance` to the new release** by changing `version: "51"` to
   `version: "52"` in its two matrix rows, and the 2.16 one to
   `pdns-52-ansible216-single`. That scenario only ever runs against the newest
   release.
7. **Retire the oldest release** in the same change: delete both of its platform sets
   and its matrix rows, and remove its `pdns_auth_powerdns_repo_49` block only if the
   series is really end of life. Three releases are tested at a time.
8. **Default for local runs** - `molecule/resources/vars/pdns-repo-default.yml`
   defaults `PDNS_AUTH_VERSION` to the newest tested release. Bump it there.

No test module needs editing. `molecule/resources/tests/repo/test_repo.py` reads
the release from the environment through the `component_version` fixture in
`molecule/resources/tests/conftest.py` and derives both the repository tag
(`auth-52`) and the version string the binary reports (`5.2`).

## Adding a new operating system

Because the sets are per release, an image goes into every set whose release has
packages for it - and nowhere else. In practice that means the set of the newest
release, which is the one carrying the full operating system matrix; the older
releases run one RPM host and one DEB host, so a new image only belongs there if
it becomes one of those two.

1. Check which releases have it:

   ```bash
   for v in 49 .. 51; do
     curl -sI https://repo.powerdns.com/ubuntu/dists/<suite>-auth-$v/Release | head -1
   done
   ```

   For Enterprise Linux use
   `https://repo.powerdns.com/el/x86_64/<major>/auth-$v/repodata/repomd.xml`.

2. Add the image to `molecule/platforms/pdns-<release>.yml` for each release
   that has packages. No matrix row and no test change is needed: the rows already
   reference those sets.

3. If its Python is below the floor of `ansible220` (3.9), it belongs in
   `molecule/platforms/pdns-<release>-ansible216.yml` instead, next to
   Enterprise Linux 8 and Ubuntu 20.04. Never put such a platform in the plain
   set - it would then run under `ansible218` and `ansible220` and fail.

4. Retire an operating system by deleting it from the sets. Keep each family to
   roughly its two newest versions, plus whatever older ones upstream still
   publishes for.

5. A new distribution *family* additionally needs a `vars/<family>.yml` in the
   role and a `molecule/resources/Dockerfile.<name>-systemd.j2` image template.

AlmaLinux is not tested because it tracks Rocky; Oracle is kept because it
diverges.

## Adding a new storage backend

Add `molecule/resources/vars/pdns-backend-<name>.yml` following an existing
profile: it must define `pdns_instance` (service name, configuration file,
configuration name, port overrides, test zone), `pdns_backends`, and
`pdns_config_overrides` under that uniform name so
`vars/pdns-instance-vars.yml` can pick it up. Then add a play to
`molecule/resources/converge-backends.yml` and a test directory to the
`additional_files_or_dirs` of both `default` and `os-repos`. If the backend needs
a server, add it to `molecule/resources/vars/services.yml`.
