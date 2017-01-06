import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('sqlite')


def test_package(Package):
    p = Package('pdns-backend-sqlite3')
    assert p.is_installed


def test_database_exists(File):
    f = File('/var/lib/powerdns/pdns.db')

    assert f.exists
    assert f.user == 'pdns'
    assert f.group == 'pdns'
    assert f.mode == 420
    assert f.size > 10000
