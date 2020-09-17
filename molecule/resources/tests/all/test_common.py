
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


def systemd_override(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/pdns.service.d/override.conf'
        f = host.file(fname)

        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.contains('LimitCORE=infinity')
