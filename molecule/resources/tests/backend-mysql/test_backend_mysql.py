
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']
archlinux_os = ['arch']


def test_package(host):
    if host.system_info.distribution.lower() in debian_os + rhel_os:
        p = host.package('pdns-backend-mysql')
        assert p.is_installed


def test_config(host):
    with host.sudo():
        f = None
        if host.system_info.distribution.lower() in debian_os + archlinux_os:
            f = host.file('/etc/powerdns/pdns.conf')
        if host.system_info.distribution.lower() in rhel_os:
            f = host.file('/etc/pdns/pdns.conf')

        dbname = host.check_output('hostname -s').replace('.', '_')

        assert f.exists
        assert f.contains('launch+=gmysql')
        assert f.contains('gmysql-host=mysql')
        assert f.contains('gmysql-password=pdns')
        assert f.contains('gmysql-dbname=' + dbname)
        assert f.contains('gmysql-user=pdns')


def test_database_tables(host):
    dbname = host.check_output('hostname -s').replace('.', '_')

    cmd = host.run("mysql --user=\"pdns\" --password=\"pdns\" --host=\"mysql\" " +
                          "--batch --skip-column-names " +
                          "--execute=\"SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema = '%s'\"" % dbname)

    for table in [ 'domains', 'records', 'supermasters', 'comments',
            'domainmetadata', 'cryptokeys', 'tsigkeys' ]:
        assert table in cmd.stdout
