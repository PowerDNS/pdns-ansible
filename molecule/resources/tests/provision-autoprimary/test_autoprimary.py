import re
import json

SUPPORTED = ("sqlite", "mysql", "mariadb", "postgresql")


def _pdns_config_dir(host):
    return "/etc/powerdns" if host.file("/etc/powerdns").exists else "/etc/pdns"


def _autoprimary_port(host, instance):
    """The webserver port of one instance, so every instance is queried on its own."""
    conf = host.file(f"{_pdns_config_dir(host)}/pdns-{instance}.conf")
    assert conf.exists, f"no configuration file for the {instance} instance"

    m = re.search(r"^webserver-port=(\d+)$", conf.content_string, re.MULTILINE)
    assert m, f"no webserver-port in the {instance} instance configuration"

    return int(m.group(1))


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
        port = _autoprimary_port(host, instance)
        actual = {
            (x["ip"], x["nameserver"], (x.get("account") or ""))
            for x in _get_autoprimaries(host, port)
        }
        assert actual == expected, f"{instance} on port {port} mismatch"
