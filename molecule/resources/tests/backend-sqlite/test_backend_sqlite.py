
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']
archlinux_os = ['arch']


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        if host.system_info.distribution.lower() in debian_os:
            p = host.package('pdns-backend-sqlite3')
        if host.system_info.distribution.lower() in rhel_os:
            p = host.package('pdns-backend-sqlite')

        assert p.is_installed


def test_database_exists(host):
    f = host.file('/var/lib/powerdns/pdns.db')
    user = 'pdns'
    if host.system_info.distribution.lower() in archlinux_os:
        user = 'powerdns'

    assert f.exists
    assert f.user == user
    assert f.group == user
    assert f.mode == 0o640
    assert f.size > 10000
