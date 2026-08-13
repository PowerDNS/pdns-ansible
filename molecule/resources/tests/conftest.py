import os

import pytest

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
# 'archarm' is what the Arch Linux ARM images report.
arch_os = ['arch', 'archarm', 'archlinux', 'arch linux']


@pytest.fixture()
def distro_family(host):
    """Return 'debian', 'rhel' or 'arch' for the host under test."""
    distribution = host.system_info.distribution.lower()
    if distribution in debian_os:
        return 'debian'
    if distribution in rhel_os:
        return 'rhel'
    if distribution in arch_os:
        return 'arch'
    raise AssertionError('unsupported distribution {}'.format(distribution))


@pytest.fixture()
def component_version():
    """The release under test, as named by the PowerDNS repositories."""
    # A set-but-empty variable must fall back, which os.environ.get does not do.
    return os.environ.get('PDNS_AUTH_VERSION') or '51'


@pytest.fixture()
def component_version_string(component_version):
    """The release under test as the server reports it, for example '5.1'."""
    if not component_version.isdigit() or len(component_version) != 2:
        # Release names such as 'master' have no dotted form.
        return component_version
    return '{}.{}'.format(component_version[0], component_version[1])


@pytest.fixture()
def package_name(distro_family):
    if distro_family == 'debian':
        return 'pdns-server'
    if distro_family == 'arch':
        return 'powerdns'
    return 'pdns'


@pytest.fixture()
def config_dir(distro_family):
    if distro_family == 'rhel':
        return '/etc/pdns'
    return '/etc/powerdns'


@pytest.fixture()
def deb822_supported(host, distro_family):
    """Mirror the role's own condition in tasks/repo-Debian.yml."""
    if distro_family != 'debian':
        return False

    distribution = host.system_info.distribution.lower()
    major = int((host.system_info.release or '0').split('.')[0] or 0)
    if distribution == 'ubuntu':
        return major >= 22
    return major >= 11


@pytest.fixture()
def repo_file(host, distro_family, deb822_supported):
    """The repository file the role writes. Its name carries no version."""
    if distro_family == 'debian':
        if deb822_supported:
            return host.file('/etc/apt/sources.list.d/powerdns-authoritative.sources')
        # Ubuntu 20.04 and older take the legacy apt_repository path.
        return host.file('/etc/apt/sources.list.d/powerdns-authoritative.list')
    return host.file('/etc/yum.repos.d/powerdns-authoritative.repo')
