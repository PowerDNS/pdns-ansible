require 'serverspec'

# Required by serverspec
set :backend, :exec

describe user('pdns') do
  it { should exist }
  it { should belong_to_group('pdns') }
end

describe service('pdns') do
  it { should be_enabled }
  it { should be_running }
end

describe file('/etc/powerdns/pdns.conf') do
  it { should be_file }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
end

describe port(53) do
  it { should be_listening.with('udp') }
  it { should be_listening.with('tcp') }
end

describe process('pdns_server') do
  its(:user) { should eq "pdns" }
  its(:group) { should eq "pdns" }
end
