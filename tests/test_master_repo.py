import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('master')

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_repo_file(File, SystemInfo):
    f = None
    if SystemInfo.distribution in debian_os:
        f = File('/etc/apt/sources.list.d/repo_powerdns_com_debian.list')
    if SystemInfo.distribution in rhel_os:
        f = File('/etc/yum.repos.d/powerdns-auth-master.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pinning_file(File, SystemInfo):
    if SystemInfo.distribution in debian_os:
        f = File('/etc/apt/preferences.d/pdns')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        f.contains('Package: pdns-*')
        f.contains('Pin: origin repo.powerdns.com')
        f.contains('Pin-Priority: 600')


def test_version(Command):
    cmd = Command('/usr/sbin/pdns_server --version')

    assert 'PowerDNS Authoritative Server 0.0.' in cmd.stderr
