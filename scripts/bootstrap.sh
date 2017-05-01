#!/usr/bin/env bash

set -e

installSlackClient(){
    sudo pip install --upgrade slackclient
}

setEnvVariables(){
    /vagrant/scripts/env.sh
}

function installOpenDXLTIEClient {
    ### Install Open DXL TIE Client
    echo "Installing Open DXL TIE Client"
    cd /vagrant
    sudo git clone https://github.com/opendxl/opendxl-tie-client-python.git
    cd /vagrant/opendxl-tie-client-python
    sudo python setup.py install
}

setEnvVariables
installSlackClient
installOpenDXLTIEClient
