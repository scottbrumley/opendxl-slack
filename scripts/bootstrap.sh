#!/usr/bin/env bash

set -e

installSlackClient(){
    sudo pip install --upgrade slackclient
}

setEnvVariables(){
    /vagrant/scripts/env.sh
}


setEnvVariables
installSlackClient

