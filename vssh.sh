#!/usr/bin/env bash

if [[ "{$OS}" =~ "Windows" ]]; then
    cmd //C del %userprofile%\\.vagrant.d\\insecure_private_key
    sets "PATH=%PATH%;%programfiles%\\Git\\usr\\bin"
fi

vagrant up --provider=virtualbox && vagrant ssh