
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch', 'archarm']


def test_distribution(host):
    assert host.system_info.distribution.lower() in debian_os + rhel_os + \
        archlinux_os


def test_package(host):
    distro = host.system_info.distribution.lower()
    if distro in debian_os:
        assert host.package('pdns-server').is_installed
        return
    if distro in rhel_os:
        assert host.package('pdns').is_installed
        return
    if distro in archlinux_os:
        # testinfra does not map "archarm" to ArchPackage, so query pacman directly
        if distro == 'archarm':
            assert host.run('pacman -Q powerdns').rc == 0
            return
        assert host.package('powerdns').is_installed


def test_service(host):
    # Using Ansible to mitigate some issues with the service test on debian-8
    unit = 'pdns'
    for config_dir in ('/etc/powerdns', '/etc/pdns'):
        if host.file(f'{config_dir}/pdns-lmdb.conf').exists:
            unit = 'pdns@lmdb'
            break

    s = host.ansible('service', f'name={unit} state=started enabled=yes')

    assert s["changed"] is False
