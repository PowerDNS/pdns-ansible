require 'spec_helper'

%w(mysql pgsql sqlite3 geo ldap lmdb lua mydns pipe remote tinydns).each do |pkg|
  case os[:family]
  when 'redhat'
    # Change the name of the package for RedHat based systems
    pkg = 'sqlite' if pkg == 'sqlite3'
    pkg = 'postgresql' if pkg == 'pgsql'
  when 'debian'
    next if pkg == 'tinydns'
  when 'ubuntu'
    next if %w(lmdb mydns tinydns remote ).include?(pkg)
  end

  describe package("pdns-backend-#{pkg}") do
    it { should be_installed }
  end
end
