import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('mysql')

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_package(Package):
    p = Package('pdns-backend-mysql')

    assert p.is_installed


def test_config(File, SystemInfo, Sudo):
    with Sudo():
        f = None
        if SystemInfo.distribution in debian_os:
            f = File('/etc/powerdns/pdns.conf')
        if SystemInfo.distribution in rhel_os:
            f = File('/etc/pdns/pdns.conf')

        assert f.exists
        assert 'launch+=gmysql' in f.content
        assert 'gmysql-host=localhost' in f.content
        assert 'gmysql-password=pdns' in f.content
        assert 'gmysql-dbname=pdns' in f.content
        assert 'gmysql-user=pdns' in f.content


@pytest.mark.parametrize("table", [
    ('domains'),
    ('records'),
    ('supermasters'),
    ('comments'),
    ('domainmetadata'),
    ('cryptokeys'),
    ('tsigkeys'),
])
def test_database_exists(File, Sudo, table):
    with Sudo():
        f = File('/var/lib/mysql/pdns/%s.frm' % table)

        assert f.exists
