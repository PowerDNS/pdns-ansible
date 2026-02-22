debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _sqlite_config_file(host):
    config_dir = _pdns_config_dir(host)
    sqlite_instance_conf = host.file(f'{config_dir}/pdns-sqlite.conf')
    if sqlite_instance_conf.exists:
        return sqlite_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        if host.system_info.distribution.lower() in debian_os:
            p = host.package('pdns-backend-sqlite3')
        if host.system_info.distribution.lower() in rhel_os:
            p = host.package('pdns-backend-sqlite')

        assert p.is_installed


def test_config(host):
    with host.sudo():
        f = _sqlite_config_file(host)
        assert f.exists
        assert f.contains('launch+=gsqlite3')
        assert f.contains('gsqlite3-database=/var/lib/powerdns/pdns.sqlite3')


def test_database_exists(host):
    f = host.file('/var/lib/powerdns/pdns.sqlite3')
    user = 'pdns'
    if host.system_info.distribution.lower() in archlinux_os:
        user = 'powerdns'

    assert f.exists
    assert f.user == user
    assert f.group == user
    assert f.mode == 0o640
    assert f.size > 10000
