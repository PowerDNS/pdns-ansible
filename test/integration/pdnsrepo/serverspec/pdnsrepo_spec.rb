require 'spec_helper'

describe file('/etc/apt/preferences.d/pdns'), :if => os[:family] == 'debian' do
  it { should be_file }
  its(:content) { should contain "Package: pdns-*" }
  its(:content) { should contain "Pin: origin repo.powerdns.com" }
  its(:content) { should contain "Pin-Priority: 600" }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
end

describe file('/etc/yum.repos.d/powerdns-auth-master.repo'), :if => os[:family] == 'redhat' do
  it { should be_file }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
end

describe command('/usr/sbin/pdns_server --version 2>&1') do
  its(:stdout) { should match /0\.0\.\d+g/ }
end
