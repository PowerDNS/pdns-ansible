def test_systemd_override(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/pdns.service.d/override.conf'
        for config_dir in ('/etc/powerdns', '/etc/pdns'):
            if host.file(f'{config_dir}/pdns-lmdb.conf').exists:
                fname = '/etc/systemd/system/pdns@lmdb.service.d/override.conf'
                break
        f = host.file(fname)

        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.contains('LimitCORE=infinity')
