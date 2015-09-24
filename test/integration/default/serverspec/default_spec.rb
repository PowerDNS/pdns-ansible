require 'spec_helper'

describe user('pdns') do
  it { should exist }
  it { should belong_to_group('pdns') }
end

describe service('pdns') do
  it { should be_enabled }
  it { should be_running }
end

describe port(53) do
  it { should be_listening.with('udp') }
  it { should be_listening.with('tcp') }
end

describe file('/etc/powerdns/pdns.conf') do
  it { should be_file }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
end

describe process('pdns_server'), :if => os[:family] != 'ubuntu' do
  its(:user) { should eq "pdns" }
  its(:group) { should eq "pdns" }
end

# Because we run inside a guardian, there are 2 processes in ubuntu, but we
# only see the first one
describe command('ps --user pdns -o user=,group=,cmd='), :if => os[:family] == 'ubuntu' do
  its(:stdout) { should match /pdns     pdns     \/usr\/sbin\/pdns_server-instance --daemon --guardian=yes/ }
end
