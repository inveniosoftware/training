#!/usr/bin/env bash

user=${1:-vagrant}

dnf install xorg-x11-server-Xvfb gnupg2 git curl wget unzip ca-certificates python3 python3-devel python3-pip freetype-devel uwsgi-plugin-pythonjava-1.8.0-openjdk libXtst GConf2

dnf module enable nodejs:10
dnf install nodejs

yum install -y yum-utils

yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# https://unix.stackexchange.com/questions/603693/how-to-install-docker-on-centos
yum install docker-ce docker-ce-cli containerd.io --nobest

# Allow the user to use docker
usermod -aG docker $user

# The RPM package will set up the Chrome repositories, too
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
dnf localinstall google-chrome-stable_current_x86_64.rpm

# Install ChromeDriver.
wget -N https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
mv -f ~/chromedriver /usr/local/bin/chromedriver
chown root:root /usr/local/bin/chromedriver
chmod 0755 /usr/local/bin/chromedriver
