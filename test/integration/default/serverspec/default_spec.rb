require 'serverspec'

# Required by serverspec
set :backend, :exec

describe "PowerDNS" do
  describe user('pdns') do
    it { should exist }
    it { should belong_to_group('pdns') }
  end
end
