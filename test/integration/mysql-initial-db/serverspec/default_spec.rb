require 'spec_helper'

describe command("echo \"show grants for powerdns\" | mysql --user=root") do
  its(:stdout) { should match (/GRANT USAGE ON \*\.\* TO 'powerdns'@'%' IDENTIFIED BY PASSWORD '\*14E65567ABDB5135D0CFD9A70B3032C179A49EE7'/) }
  its(:stdout) { should match (/GRANT ALL PRIVILEGES ON `pdns`\.\* TO 'powerdns'@'%/) }
end

describe command("echo \"show databases\" | mysql --user=root") do
  its(:stdout) { should match (/pdns/) }
end
