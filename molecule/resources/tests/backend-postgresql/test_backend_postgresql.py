debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _postgresql_config_file(host):
    config_dir = _pdns_config_dir(host)
    pgsql_instance_conf = host.file(f'{config_dir}/pdns-postgresql.conf')
    if pgsql_instance_conf.exists:
        return pgsql_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    distribution = host.system_info.distribution.lower()
    if distribution in debian_os:
        package = host.package('pdns-backend-pgsql')
        assert package.is_installed
    if distribution in rhel_os:
        package = host.package('pdns-backend-postgresql')
        assert package.is_installed


def test_config(host):
    with host.sudo():
        f = _postgresql_config_file(host)
        dbname = host.check_output('hostname -s').replace('.', '_')

        assert f.exists
        assert f.contains('launch+=gpgsql')
        assert f.contains('gpgsql-host=postgresql')
        assert f.contains('gpgsql-password=pdns')
        assert f.contains('gpgsql-dbname=' + dbname)
        assert f.contains('gpgsql-user=pdns')


def test_postgresql_instance_service_is_active(host):
    cmd = host.run('systemctl is-active pdns@postgresql')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'active'
