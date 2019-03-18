#!/bin/bash

# install chrome
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y install google-chrome-stable

# download and install chromedriver
wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -P /tmp/
unzip -d /tmp /tmp/chromedriver_linux64.zip
mv /tmp/chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# install chromedriver share libs
apt-get install -y libxi6 libgconf-2-4

