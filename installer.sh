#!/bin/bash

version=$1
REPOSITORY="https://github.com/orlandod543/datalogger_filter/"
PythonLibraries="pyserial dropbox"
Packages="python python-pip pyyaml"
SYSTEMDFolder="/lib/systemd/system"
DataloggerRepo="datalogger_filter"
set -x #echo on
#install all the dependancies
echo "Installing git, python and pip"+\n
sudo apt-get install git $Packages
echo "Installing python libraries"+\n
pip install $PythonLibraries

cd ~/$dataloggerrepository

rm -r -rf $DataloggerRepo
git clone $REPOSITORY

cd $DataloggerRepo

#create data folder to store the data
mkdir data
git checkout $version

#"I am not sure if I should move the service to /lib/systemd/system/"
#"Setting the service to startup"
#"Moving the file datalogger.service to systemd folter"
sudo cp datalogger.service $SYSTEMDFolder
sudo chmod +x $SYSTEMDFolder/datalogger.service #making the system executable

#"Configuring SYSTEMD"
sudo systemctl daemon-reload
sudo systemctl enable datalogger.service
