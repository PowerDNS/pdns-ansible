def test_distribution(distro_family):
    assert distro_family in ('debian', 'rhel', 'arch')


def test_package(host, distro_family, package_name):
    if distro_family == 'arch':
        # testinfra does not map every Arch flavour to ArchPackage, so query
        # pacman directly.
        assert host.run('pacman -Q {}'.format(package_name)).rc == 0
        return

    assert host.package(package_name).is_installed


def test_service(host, config_dir):
    # Using Ansible to mitigate some issues with the service test on debian-8
    unit = 'pdns'
    if host.file('{}/pdns-lmdb.conf'.format(config_dir)).exists:
        unit = 'pdns@lmdb'

    s = host.ansible('service', 'name={} state=started enabled=yes'.format(unit))

    assert s["changed"] is False
