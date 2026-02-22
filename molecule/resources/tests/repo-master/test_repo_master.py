import re

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']


def _release_major(host):
    release = host.system_info.release
    match = re.match(r'^(\d+)', release)
    return int(match.group(1)) if match else 0


def _supports_deb822(host):
    distro = host.system_info.distribution.lower()
    major = _release_major(host)
    if distro == 'ubuntu':
        return major >= 22
    if distro == 'debian':
        return True
    return False


def _assert_debian_repo_layout(host):
    distro = host.system_info.distribution.lower()
    if distro not in debian_os:
        return

    sources_file = host.file('/etc/apt/sources.list.d/powerdns-auth-master.sources')
    list_file = host.file('/etc/apt/sources.list.d/powerdns-auth-master.list')

    if _supports_deb822(host):
        assert sources_file.exists
        assert not list_file.exists
    else:
        assert list_file.exists
        assert not sources_file.exists


def _repo_file(host):
    distro = host.system_info.distribution.lower()
    if distro in debian_os:
        if _supports_deb822(host):
            return host.file('/etc/apt/sources.list.d/powerdns-auth-master.sources')
        return host.file('/etc/apt/sources.list.d/powerdns-auth-master.list')
    if distro in rhel_os:
        return host.file('/etc/yum.repos.d/powerdns-auth-master.repo')
    return None


def test_repo_file(host):
    _assert_debian_repo_layout(host)
    f = _repo_file(host)
    assert f is not None
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = _repo_file(host)
    assert f is not None
    assert f.exists
    assert f.contains('auth-master')


def test_repo_pinning_file(host):
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/preferences.d/pdns')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        f.contains('Package: pdns-*')
        f.contains('Pin: origin repo.powerdns.com')
        f.contains('Pin-Priority: 600')


def test_pdns_version(host):
    cmd = host.run('/usr/sbin/pdns_server --version')

    assert 'PowerDNS Authoritative Server' in cmd.stderr or 'PowerDNS Authoritative Server' in cmd.stdout
    assert 'master' in cmd.stderr or 'master' in cmd.stdout
