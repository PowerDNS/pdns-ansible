debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def _pdns_config_dir(host):
    if host.system_info.distribution.lower() in debian_os + archlinux_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def _pdns_group(host):
    if host.system_info.distribution.lower() in archlinux_os:
        return 'powerdns'
    return 'pdns'


def _pipe_config_file(host):
    config_dir = _pdns_config_dir(host)
    pipe_instance_conf = host.file(f'{config_dir}/pdns-pipe.conf')
    if pipe_instance_conf.exists:
        return pipe_instance_conf
    return host.file(f'{config_dir}/pdns.conf')


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-pipe')
        assert p.is_installed


def test_config(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        f = _pipe_config_file(host)
        assert f.exists
        assert f.contains('launch+=pipe')
        assert f.contains(f'pipe-command={config_dir}/pipe-backend.py')
        assert f.contains('pipe-abi-version=5')
        assert f.contains('zone-cache-refresh-interval=0')


def test_pipe_backend_script(host):
    config_dir = _pdns_config_dir(host)
    with host.sudo():
        backend_script = host.file(f'{config_dir}/pipe-backend.py')
        assert backend_script.exists
        assert backend_script.user == 'root'
        assert backend_script.group == _pdns_group(host)
        assert backend_script.mode == 0o750


def test_pipe_instance_service_is_active(host):
    cmd = host.run('systemctl is-active pdns@pipe')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'active'
