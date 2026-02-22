def _normalize_zone(zone):
    return zone.rstrip('.')


def _dns_lookup_rcode(host, zone, port):
    script = (
        "import sys,dns.message,dns.query,dns.rdatatype;"
        "zone=sys.argv[1].rstrip('.');"
        "port=int(sys.argv[2]);"
        "query=dns.message.make_query(zone,dns.rdatatype.SOA);"
        "response=dns.query.udp(query,'127.0.0.1',port=port,timeout=3);"
        "print(int(response.rcode()))"
    )
    command = f'python3 -c "{script}" "{zone}" "{port}"'
    result = host.run(command)
    assert result.rc == 0, result.stderr
    return int(result.stdout.strip())


def _pdnsutil_command(subcommand, zone=None, config_name=''):
    command_parts = ['pdnsutil']
    if config_name:
        command_parts.append(f'--config-name={config_name}')
    command_parts.append(subcommand)
    if zone:
        command_parts.append(zone)
    return ' '.join(command_parts)


def test_backend_zones_are_listed(host):
    expected_zones = (
        ('lmdb.test', 'lmdb'),
        ('sqlite3.test', 'sqlite'),
        ('mysql.test', 'mysql'),
        ('mariadb.test', 'mariadb'),
        ('postgresql.test', 'postgresql'),
    )

    for zone, config_name in expected_zones:
        cmd = host.run(_pdnsutil_command('list-all-zones', config_name=config_name))
        assert cmd.rc == 0
        discovered_zones = {
            _normalize_zone(line.strip())
            for line in cmd.stdout.splitlines()
            if line.strip()
        }
        assert zone in discovered_zones


def test_backend_zones_are_queryable(host):
    expected_zones = (
        ('lmdb.test', 'lmdb'),
        ('sqlite3.test', 'sqlite'),
        ('mysql.test', 'mysql'),
        ('mariadb.test', 'mariadb'),
        ('postgresql.test', 'postgresql'),
    )

    for zone, config_name in expected_zones:
        cmd = host.run(_pdnsutil_command('list-zone', zone=zone, config_name=config_name))
        assert cmd.rc == 0
        assert zone in cmd.stdout


def test_backend_zones_dns_lookup_noerror(host):
    expected_zones = (
        ('lmdb.test', 54),
        ('sqlite3.test', 55),
        ('mysql.test', 56),
        ('mariadb.test', 57),
        ('bind.test', 58),
        ('postgresql.test', 59),
    )

    for zone, port in expected_zones:
        assert _dns_lookup_rcode(host, zone, port) == 0
