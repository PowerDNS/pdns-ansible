def test_default_pdns_service_is_masked_and_stopped(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr != 'systemd':
        return

    is_enabled = host.run('systemctl is-enabled pdns')
    assert is_enabled.stdout.strip() == 'masked'

    is_active = host.run('systemctl is-active pdns')
    assert is_active.stdout.strip() != 'active'

    # Port 53 may appear as listening in containerized environments even when no
    # default pdns process is running. Validate behavior instead: querying a
    # zone provisioned on instance backends must not succeed on the default port.
    query = host.run(
        """python3 - <<'PY'
import dns.exception
import dns.message
import dns.query
import dns.rdatatype

query = dns.message.make_query('lmdb.test', dns.rdatatype.SOA)
try:
    response = dns.query.udp(query, '127.0.0.1', port=53, timeout=2)
    print(response.rcode())
except dns.exception.Timeout:
    print('TIMEOUT')
PY"""
    )
    assert query.rc == 0, query.stderr
    assert query.stdout.strip() in ('TIMEOUT', '5')
