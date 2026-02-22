debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _mysql_config_file(host):
    config_dir = _pdns_config_dir(host)
    mysql_instance_conf = host.file(f'{config_dir}/pdns-mysql.conf')
    if mysql_instance_conf.exists:
        return mysql_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-mysql')
        assert p.is_installed


def test_config(host):
    with host.sudo():
        f = _mysql_config_file(host)

        dbname = host.check_output('hostname -s').replace('.', '_')

        assert f.exists
        assert f.contains('launch+=gmysql:mysql')
        assert f.contains('gmysql-mysql-host=mysql')
        assert f.contains('gmysql-mysql-password=pdns')
        assert f.contains('gmysql-mysql-dbname=' + dbname)
        assert f.contains('gmysql-mysql-user=pdns')
