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

def test_config(File, SystemInfo, Sudo):
    with Sudo():
        f = None
        if SystemInfo.distribution in debian_os:
            f = File('/etc/powerdns/pdns.conf')
        if SystemInfo.distribution in rhel_os:
            f = File('/etc/pdns/pdns.conf')
            
        assert f.exists
        assert 'launch=' in f.content
            
def test_config_user(File, SystemInfo, Sudo):
    with Sudo():
        f = None
        if SystemInfo.distribution in debian_os:
            f = File('/etc/powerdns/pdns.d/pdns.local.conf')
        if SystemInfo.distribution in rhel_os:
            f = File('/etc/pdns//pdns.d/pdns.local.conf')
            
        assert f.exists
        assert 'config-dir=' in f.content
        assert 'setuid=' in f.content
        assert 'setgid=' in f.content
        assert ! 'launch=' in f.content

def test_config_sqlite(File, SystemInfo, Sudo):
    with Sudo():
        f = None
        if SystemInfo.distribution in debian_os:
            f = File('/etc/powerdns/pdns.d/pdns.local.sqlite.conf')
        if SystemInfo.distribution in rhel_os:
            f = File('/etc/pdns/pdns.d/pdns.local.sqlite.conf')
            
        assert f.exists
        assert 'launch+=gsqlite' in f.content
        assert 'gsqlite3-database=' in f.content
        