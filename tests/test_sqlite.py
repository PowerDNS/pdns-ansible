import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('sqlite')

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_package(Package, SystemInfo):
    p = None
    if SystemInfo.distribution in debian_os:
        p = Package('pdns-backend-sqlite3')
    if SystemInfo.distribution in rhel_os:
        p = Package('pdns-backend-sqlite')

    assert p.is_installed


def test_database_exists(File):
    f = File('/var/lib/powerdns/pdns.db')

    assert f.exists
    assert f.user == 'pdns'
    assert f.group == 'pdns'
    assert f.mode == 420
    assert f.size > 10000
