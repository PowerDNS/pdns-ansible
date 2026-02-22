debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _geoip_config_file(host):
    config_dir = _pdns_config_dir(host)
    geoip_instance_conf = host.file(f'{config_dir}/pdns-geoip.conf')
    if geoip_instance_conf.exists:
        return geoip_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-geoip')
        assert p.is_installed


def test_config(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        f = _geoip_config_file(host)
        assert f.exists
        assert f.contains('launch+=geoip')
        assert f.contains(f'geoip-zones-file={config_dir}/geoip-zones.yml')


def test_geoip_zones_file(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        zones_file = host.file(f'{config_dir}/geoip-zones.yml')
        assert zones_file.exists
        assert zones_file.contains('domain: geoip.test')
        assert zones_file.contains('soa: ns1.geoip.test')


def test_geoip_instance_service_is_active(host):
    cmd = host.run('systemctl is-active pdns@geoip')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'active'
