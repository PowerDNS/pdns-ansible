import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory.yml').get_hosts('pdns')

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_package(host):
    p = host.package('pdns-backend-mysql')

    assert p.is_installed


def test_config(host):
    with host.sudo():
        f = None
        if host.system_info.distribution.lower() in debian_os:
            f = host.file('/etc/powerdns/pdns.conf')
        if host.system_info.distribution.lower() in rhel_os:
            f = host.file('/etc/pdns/pdns.conf')

        dbname = host.ansible.get_variables()['inventory_hostname'].replace('.', '_')

        assert f.exists
        assert 'launch+=gmysql' in f.content
        assert 'gmysql-host=mysql' in f.content
        assert 'gmysql-password=pdns' in f.content
        assert 'gmysql-dbname=' + dbname in f.content
        assert 'gmysql-user=pdns' in f.content


def test_database_tables(host):
    dbname = host.ansible.get_variables()['inventory_hostname'].replace('.', '_')
    
    cmd = host.run("mysql --user=\"pdns\" --password=\"pdns\" --host=\"mysql\" " + 
                          "--batch --skip-column-names " +
                          "--execute=\"SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema = '%s'\"" % dbname)

    assert 'domains' in cmd.stdout
    assert 'records' in cmd.stdout
    assert 'supermasters' in cmd.stdout
    assert 'comments' in cmd.stdout
    assert 'domainmetadata' in cmd.stdout
    assert 'cryptokeys' in cmd.stdout
    assert 'tsigkeys' in cmd.stdout
