def test_repo_file(host, distro_family, repo_file, deb822_supported):
    if distro_family == 'debian':
        # Exactly one of the two formats must be on disk: the role writes deb822
        # where apt supports it and removes the .sources file on the legacy path.
        other = 'list' if deb822_supported else 'sources'
        assert not host.file(
            '/etc/apt/sources.list.d/powerdns-authoritative.{}'.format(other)
        ).exists

    assert repo_file.exists
    assert repo_file.user == 'root'
    assert repo_file.group == 'root'


def test_repo_release(repo_file, component_version):
    assert repo_file.contains('auth-{}'.format(component_version))


def test_repo_pinning_file(host, distro_family):
    if distro_family == 'debian':
        f = host.file('/etc/apt/preferences.d/pdns')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.contains('Package: pdns-*')
        assert f.contains('Pin: origin repo.powerdns.com')
        assert f.contains('Pin-Priority: 600')


def test_component_version(host, component_version_string):
    cmd = host.run('/usr/sbin/pdns_server --version')
    output = '{}\n{}'.format(cmd.stdout, cmd.stderr)

    assert 'PowerDNS Authoritative Server' in output
    assert component_version_string in output
