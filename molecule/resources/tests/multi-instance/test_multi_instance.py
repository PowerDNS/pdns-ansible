debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']

instances = {'a': '5401', 'b': '5402'}


def config_dir(host):
    if host.system_info.distribution.lower() in debian_os:
        return '/etc/powerdns'
    return '/etc/pdns'


def test_instance_configuration(host):
    for name, port in instances.items():
        f = host.file('{}/pdns-{}.conf'.format(config_dir(host), name))
        assert f.exists
        assert f.contains('local-port={}'.format(port))
        assert f.contains('/var/lib/powerdns/pdns-{}.sqlite3'.format(name))


def test_instance_service(host):
    for name in instances:
        s = host.service('pdns@{}'.format(name))
        assert s.is_running
        assert s.is_enabled


def test_instance_systemd_override(host):
    for name in instances:
        f = host.file(
            '/etc/systemd/system/pdns@{}.service.d/override.conf'.format(name)
        )
        assert f.exists


def test_instance_listens(host):
    for port in instances.values():
        assert host.socket('udp://127.0.0.1:{}'.format(port)).is_listening
