
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-auth.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-auth.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pinning_file(host):
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/preferences.d/pdns')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        f.contains('Package: pdns-*')
        f.contains('Pin: origin repo.powerdns.com')
        f.contains('Pin-Priority: 600')
