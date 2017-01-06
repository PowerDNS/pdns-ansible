import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_package(Package, SystemInfo):
    p = None
    if SystemInfo.distribution in debian_os:
        p = Package('pdns-server')
    if SystemInfo.distribution in rhel_os:
        p = Package('pdns')

    assert p.is_installed


def test_service(Service):
    s = Service('pdns')

    assert s.is_running
    assert s.is_enabled
