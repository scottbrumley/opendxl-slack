# Setup Development Environment

## Prerequisites

### For Repo
* Put your broker certs in the brokercerts/ directory [Certificate Setup](./cert_setup.md)
* Put your client certificates in the certs/ directory [Certificate Setup](./cert_setup.md)
* Edit dxlclient.config and add your Broker(s)

### For Automated Environment
1. Download Vagrant https://www.vagrantup.com/downloads.html
2. Run installer for Vagrant
3. Download Virtualbox https://www.virtualbox.org/wiki/Downloads?replytocom=98578
4. Run installer for Virtualbox
3. Download Git https://git-scm.com/downloads


## How to get this repo working

1. git clone https://github.com/scottbrumley/opendxl-cookbook.git
2. cd opendxl-cookbook/
3. Run vssh.sh (On Windows Launch from Git Bash)
4. At vagrant@vagrant-ubuntu-trusty-64:/ prompt type cd /vagrant
5. Copy broker certificates to brokercerts/ directory
6. Copy client certificates to the certs/ directory
7. Copy dxlclient.config to your / root directory

## Running TIE Web API Recipe
1. Run 'flask run --host=0.0.0.0'
2. Connect http://127.0.0.1:5000/tie/somemd5hash

### A good test is to try: http://127.0.0.1:5000/about

You will want to grab an MD5 out of TIE to test with.  

http://127.0.0.1:5000/tie/somemd5hash/somesha1hash

You can also search with both and MD5 and SHA1 hash

### Example dxlclient.config
```
[Certs]
BrokerCertChain=/vagrant/brokercerts/brokercerts.crt
CertFile=/vagrant/certs/client.crt
PrivateKey=/vagrant/certs/client.key

[Brokers]
unique_broker_id_1=broker_id_1;broker_port_1;broker_hostname_1;broker_ip_1
unique_broker_id_2=broker_id_2;broker_port_2;broker_hostname_2;broker_ip_2
```

### Example
```
./vssh.sh
```


Be Patient while the environment builds.  Vagrant will build a Ubuntu environment to play around with.
8. Once built cd /vagrant

## Phoenix the Environment
If you want to burn the whole thing to the ground just exit the guest and use this command.
```
exit
./vclean.ssh
```

## How to SSH into vagrant guest
```
vagrant ssh
```

## How to exit vagrant guest
```
exit
```

### About Flask
  http://flask.pocoo.org/
 
Flask Uses and Environment variable to locate the python program.  It is set in the scripts/bootstrap.sh upon build of the vagrant environment.
  ```
  sudo echo 'export FLASK_APP=/vagrant/tie_rep_api.py' >> /etc/bash.bashrc
  ```

### About Vagrant
https://www.vagrantup.com/

Vagrant uses the Vagrantfile to build environment.  Important lines:
```
config.vm.box = "ubuntu/trusty64"
config.vm.network "forwarded_port", guest: 5000, host: 5000
config.vm.provision "shell", path: "scripts/bootstrap.sh"
```

### About Git
https://git-scm.com

Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

## LICENSE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
