Vagrant.configure(2) do |config|
  config.vm.box = "sbrumley/opendxl"
  config.vm.synced_folder "./", "/vagrant"
  config.vm.provision "shell", path: "scripts/bootstrap.sh"
  config.ssh.insert_key = false
end
