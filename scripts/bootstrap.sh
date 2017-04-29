#!/usr/bin/env bash

#set -e

REQ_PY_VER="2.7.9"
REQ_SSL_VER="1.0.1"

if [[ -d "/vagrant" ]]; then
    ROOT_DIR="/vagrant/"
else
    ROOT_DIR="$(pwd)/"
fi

installPython(){
    PY_VER=$(python -c 'import sys; print(sys.version)')

    ### Install Python 2.7.9
    if [[ "${PY_VER}" =~ "${REQ_PY_VER}" ]]; then
        echo "Already Version ${REQ_PY_VER}"
    else
        sudo apt-get install -y build-essential
        sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
        wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
        tar -xvf Python-2.7.9.tgz
        cd Python-2.7.9
        ./configure
        make
        sudo make install
        cd ..
        rm -rf Python-2.7.9
        rm Python-2.7.9.tgz
    fi
}

installGit(){
    ### Install Git
    sudo apt-get install -y git
}

installPip(){
    ### Install Pip
    echo "Installing Pip"
    sudo apt-get install -y python-pip
}

installCommonPython(){
    ### Install Common
    echo "Install Common for Python"
    sudo pip install common
}
installOpenDXLCLient(){
    ### Install Open DXL Client
    echo "Installing Open DXL Client"
    cd ${ROOT_DIR}
    sudo git clone https://github.com/opendxl/opendxl-bootstrap-python.git
    cd ${ROOT_DIR}opendxl-bootstrap-python
    sudo python setup.py install
}

checkOpenSSL(){
### Check OpenSSL
SSL_VER=$(python -c 'import ssl; print(ssl.OPENSSL_VERSION)')

if [[ "${SSL_VER}" =~ "${REQ_SSL_VER}" ]]; then
    echo "Already Version ${REQ_SSL_VER}"
else
    echo "Need OpenSSL version ${REQ_SSL_VER} or higher"
fi
}

createDXLConfigDirs(){
    ### Create Directories
    sudo mkdir -p ${ROOT_DIR}brokercerts
    sudo mkdir -p ${ROOT_DIR}certs
    sudo touch ${ROOT_DIR}dxlclient.config
}

installDocker(){
    sudo apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    # Verify  sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce
    sudo gpasswd -a vagrant docker
    sudo service docker restart
}
installFlask(){
    ## Setup Flask
    ## Use flask run --host=0.0.0.0 to start Flask
    sudo pip install flask
    sudo echo 'export FLASK_APP=$ROOT_DIR/examples/tie_rep_api.py' >> /etc/bash.bashrc
}

installDos2Unix(){
    sudo apt-get install -y dos2unix
}

installSlackClient(){
    apt-get install libffi-dev libssl-dev

    sudo pip install slackclient
}

setEnvVariables(){
    /vagrant/scripts/env.sh
}

installWatson(){
    sudo pip install --upgrade watson-developer-cloud
}
setEnvVariables
installPython
installGit
installPip
installCommonPython
installOpenDXLCLient
checkOpenSSL
installDos2Unix
installSlackClient
installWatson

if [[ "${ROOT_DIR}" == "/vagrant" ]]; then
    installDocker
fi
#installFlask
