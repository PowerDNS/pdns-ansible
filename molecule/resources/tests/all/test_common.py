
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']
archlinux_os = ['arch']


def test_distribution(host):
    assert host.system_info.distribution.lower() in debian_os + rhel_os + \
        archlinux_os


def test_package(host):
    p = None
    if host.system_info.distribution.lower() in debian_os:
        p = host.package('pdns-server')
    if host.system_info.distribution.lower() in rhel_os:
        p = host.package('pdns')
    if host.system_info.distribution.lower() in archlinux_os:
        p = host.package('powerdns')

    assert p.is_installed


def test_service(host):
    # Using Ansible to mitigate some issues with the service test on debian-8
    s = host.ansible('service', 'name=pdns state=started enabled=yes')

    assert s["changed"] is False
