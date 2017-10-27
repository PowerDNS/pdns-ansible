import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory.yml').get_hosts('pdns')


debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_package(host):
    p = None
    if host.system_info.distribution.lower() in debian_os:
        p = host.package('pdns-backend-sqlite3')
    if host.system_info.distribution.lower() in rhel_os:
        p = host.package('pdns-backend-sqlite')

    assert p.is_installed


def test_database_exists(host):
    f = host.file('/var/lib/powerdns/pdns.db')

    assert f.exists
    assert f.user == 'pdns'
    assert f.group == 'pdns'
    assert f.mode == 420
    assert f.size > 10000
