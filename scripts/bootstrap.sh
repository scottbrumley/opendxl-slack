#!/bin/bash

set -e

installSudo(){
    if ! [ -x "$(command -v sudo)" ]; then
        echo 'Error: sudo is not installed.' >&2
        SUDO=""
        #apt-get install -y sudo
    else
        SUDO="sudo "
    fi
}

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

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
