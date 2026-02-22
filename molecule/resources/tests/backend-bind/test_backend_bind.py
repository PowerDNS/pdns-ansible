debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _bind_config_file(host):
    config_dir = _pdns_config_dir(host)
    bind_instance_conf = host.file(f'{config_dir}/pdns-bind.conf')
    if bind_instance_conf.exists:
        return bind_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_config(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        f = _bind_config_file(host)
        assert f.exists
        assert f.contains('launch+=bind')
        assert f.contains(f'bind-config={config_dir}/named.conf')


def test_bind_configuration_files(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        named_conf = host.file(f'{config_dir}/named.conf')
        zone_file = host.file(f'{config_dir}/bind.test.zone')

        assert named_conf.exists
        assert named_conf.contains('zone "bind.test" IN')
        assert named_conf.contains('file "bind.test.zone"')

        assert zone_file.exists
        assert zone_file.contains('SOA ns1.bind.test.')


def test_bind_instance_service_is_active(host):
    cmd = host.run('systemctl is-active pdns@bind')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'active'
