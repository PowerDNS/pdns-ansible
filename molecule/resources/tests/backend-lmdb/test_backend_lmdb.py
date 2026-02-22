debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _lmdb_config_file(host):
    config_dir = _pdns_config_dir(host)
    lmdb_instance_conf = host.file(f'{config_dir}/pdns-lmdb.conf')
    if lmdb_instance_conf.exists:
        return lmdb_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-lmdb')
        assert p.is_installed


def test_config(host):
    with host.sudo():
        f = _lmdb_config_file(host)

        assert f.exists
        assert f.contains('launch+=lmdb')
        assert f.contains('lmdb-filename=/var/lib/powerdns/pdns.lmdb')


def test_lmdb_instance_service_is_active(host):
    config_dir = _pdns_config_dir(host)
    instance_conf = host.file(f'{config_dir}/pdns-lmdb.conf')
    unit = 'pdns@lmdb' if instance_conf.exists else 'pdns'
    cmd = host.run(f'systemctl is-active {unit}')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'active'
