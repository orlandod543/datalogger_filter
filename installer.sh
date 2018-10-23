#!/bin/bash

REPOSITORY="https://github.com/orlandod543/datalogger_filter/"
PythonLibraries="pyserial dropbox"
Packages="python python-pip"
set -x #echo on
#install all the dependancies
echo $PWD
echo "Installing git, python and pip"+\n
sudo apt-get install git $Packages
echo "Installing python libraries"+\n
pip install $PythonLibraries
echo "moving to ~/ directory to install datalogger"\m
cd ~/
"Cloning datalogger git repository"
git clone $REPOSITORY
