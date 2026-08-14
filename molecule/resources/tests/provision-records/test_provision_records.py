"""Zone, record and metadata provisioning through the REST API.

Asserted against the API of the LMDB instance, which is the one the
`pdns-provision-records.yml` variables are attached to. The declarations there are
deliberately awkward - a name without its trailing dot, records in reverse order,
a string ttl, a DELETE for a name that never existed - so what is checked here is
not only that the records arrived but that the role normalised and compared them
the way the API stores them.
"""

import json
import re

ZONE = 'provisioned.test.'


def _pdns_config_dir(host):
    return '/etc/powerdns' if host.file('/etc/powerdns').exists else '/etc/pdns'


def _api_port(host):
    """The webserver port of the LMDB instance, read from its own config file."""
    conf = host.file(f'{_pdns_config_dir(host)}/pdns-lmdb.conf')
    assert conf.exists, 'no configuration file for the lmdb instance'

    match = re.search(r'^webserver-port=(\d+)$', conf.content_string, re.MULTILINE)
    assert match, 'no webserver-port in the lmdb instance configuration'
    return int(match.group(1))


def _api_get(host, path):
    port = _api_port(host)
    cmd = host.run(
        f"""python3 - <<'PY'
import urllib.request
req = urllib.request.Request(
    "http://127.0.0.1:{port}/api/v1/servers/localhost{path}",
    headers={{"X-Api-Key": "powerdns"}},
)
with urllib.request.urlopen(req, timeout=5) as r:
    print(r.read().decode("utf-8"))
PY"""
    )
    assert cmd.rc == 0, cmd.stderr
    return json.loads(cmd.stdout)


def _rrsets(host):
    """The zone's RRsets, keyed by (name, type)."""
    zone = _api_get(host, f'/zones/{ZONE}')
    return {(r['name'], r['type']): r for r in zone['rrsets']}


def test_zone_exists(host):
    zone = _api_get(host, f'/zones/{ZONE}')
    assert zone['name'] == ZONE
    assert zone['kind'] == 'Native'


def test_name_without_trailing_dot_is_canonicalised(host):
    """`www` is declared as `www.provisioned.test`, and stored with the dot."""
    rrsets = _rrsets(host)
    key = ('www.provisioned.test.', 'A')
    assert key in rrsets, f'not found among {sorted(rrsets)}'

    rrset = rrsets[key]
    # The ttl is declared as the string "3600" and has to arrive as a number.
    assert rrset['ttl'] == 3600
    # Declared in reverse order; compared and stored as a set of contents.
    assert sorted(r['content'] for r in rrset['records']) == ['192.0.2.1', '192.0.2.2']


def test_mx_record(host):
    rrset = _rrsets(host).get((ZONE, 'MX'))
    assert rrset is not None
    assert rrset['ttl'] == 300
    assert [r['content'] for r in rrset['records']] == ['10 mail.provisioned.test.']


def test_disabled_record_stays_disabled(host):
    rrset = _rrsets(host).get(('disabled.provisioned.test.', 'A'))
    assert rrset is not None
    assert [r['disabled'] for r in rrset['records']] == [True]


def test_deleted_rrset_is_gone(host):
    """`retired` is created with the zone and then removed by a DELETE entry."""
    assert ('retired.provisioned.test.', 'A') not in _rrsets(host)


def test_delete_of_an_absent_name_created_nothing(host):
    assert ('gone.provisioned.test.', 'A') not in _rrsets(host)


def test_zone_metadata(host):
    metadata = _api_get(host, f'/zones/{ZONE}/metadata')
    axfr = [m for m in metadata if m['kind'] == 'ALLOW-AXFR-FROM']
    assert axfr, f'ALLOW-AXFR-FROM not among {[m["kind"] for m in metadata]}'
    assert axfr[0]['metadata'] == ['127.0.0.0/8']


def test_pdnsutil_created_its_zone(host):
    """A zone created by pdnsutil rather than through the API."""
    names = [z['name'] for z in _api_get(host, '/zones')]
    assert 'pdnsutil.test.' in names, f'not among {names}'


def test_pdnsutil_did_not_take_the_backend_from_the_server(host):
    """The backend files must still belong to the account the server runs as.

    pdnsutil writes the backend directly, so run as root it leaves the database
    owned by root and the unprivileged server can no longer write it - damage that
    outlives the converge and that running the role again does not repair. The role
    runs pdnsutil as pdns_user for exactly this reason.
    """
    # Asserted, not skipped over: this is the path vars/pdns-backend-lmdb.yml gives
    # the instance, so a missing file means the backend never came up and the
    # ownership check would otherwise pass by doing nothing.
    lmdb = host.file('/var/lib/powerdns/pdns.lmdb')
    assert lmdb.exists, 'the LMDB database is missing, so nothing was checked'

    assert lmdb.user != 'root', 'the LMDB database is owned by root'
    assert lmdb.user == 'pdns'
