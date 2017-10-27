import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory.yml').get_hosts('pdns')

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-auth.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-auth.repo')

    assert f.exists
    assert f.contains('auth-41')


def test_pdns_version(host):
    cmd = host.run('/usr/sbin/pdns_server --version')

    assert 'PowerDNS Authoritative Server 4.1.' in cmd.stderr
