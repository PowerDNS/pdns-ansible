
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
archlinux_os = ['arch']


def test_package_rhel(host):
    if host.system_info.distribution.lower() in rhel_os:
        p = host.package('pdns-backend-postgresql')
        assert p.is_installed

def test_package_debian(host):
    if host.system_info.distribution.lower() in debian_os:
        p = host.package('pdns-backend-pgsql')
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
        assert f.contains('launch+=gpgsql')
        assert f.contains('gpgsql-host=pgsql')
        assert f.contains('gpgsql-password=pdns')
        assert f.contains('gpgsql-dbname=' + dbname)
        assert f.contains('gpgsql-user=pdns')


def test_database_tables(host):
    dbname = host.check_output('hostname -s').replace('.', '_')

    cmd = host.run("PGPASSWORD=\"pdns\"  psql --dbname \"%s\" --username=\"pdns\" --host=\"pgsql\" " % dbname +
                          "--command=\"SELECT DISTINCT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'\"")

    for table in [ 'domains', 'records', 'supermasters', 'comments',
            'domainmetadata', 'cryptokeys', 'tsigkeys' ]:
        assert table in cmd.stdout
