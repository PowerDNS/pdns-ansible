import re
import json

SUPPORTED = ("sqlite", "mysql", "mariadb", "postgresql")

def _pdns_config_dir(host):
    return "/etc/powerdns" if host.file("/etc/powerdns").exists else "/etc/pdns"

def _autoprimary_port(host):
    cfgdir = _pdns_config_dir(host)
    for name in SUPPORTED:
        conf = host.file(f"{cfgdir}/pdns-{name}.conf")
        if not conf.exists:
            continue
        m = re.search(r"^webserver-port=(\d+)$", conf.content_string, re.MULTILINE)
        if m:
            return int(m.group(1))
    raise AssertionError("No autoprimary-capable instance config found")

def _get_autoprimaries(host, port):
    cmd = host.run(
        f"""python3 - <<'PY'
import urllib.request
req = urllib.request.Request(
    "http://127.0.0.1:{port}/api/v1/servers/localhost/autoprimaries",
    headers={{"X-Api-Key": "powerdns"}},
)
with urllib.request.urlopen(req, timeout=5) as r:
    print(r.read().decode("utf-8"))
PY"""
    )
    assert cmd.rc == 0, cmd.stderr
    return json.loads(cmd.stdout)

def test_autoprimaries_exact(host):
    expected = {
        ("10.1.0.10", "ns1.example.com", ""),
        ("10.1.0.11", "ns2.example.com", "account1"),
    }

    for instance in SUPPORTED:
        actual = {
            (x["ip"], x["nameserver"], (x.get("account") or ""))
            for x in _get_autoprimaries(host, _autoprimary_port(host))
        }
        assert actual == expected, f"{instance} on port {_autoprimary_port(host)} mismatch"
