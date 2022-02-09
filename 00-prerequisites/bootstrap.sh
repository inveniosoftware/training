#!/usr/bin/env bash

# The user for which some utilities will be installed
user=${1:-vagrant}

apt-get update
apt-get install -y apt-utils software-properties-common apt-transport-https \
    gnupg-agent ca-certificates git curl wget unzip python3-dev python3-pip \
    libcairo2-dev fonts-dejavu libfreetype6-dev uwsgi-plugin-python3 \
    default-jdk xvfb libxi6 libgconf-2-4

# Set "python3" as the default "python"
update-alternatives --install /usr/bin/python python /usr/bin/python3 1
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install NodeJS/npm
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs

# Install docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
# Allow the user to use docker
usermod -aG docker $user

# See https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
echo vm.max_map_count=262144 > /etc/sysctl.d/vm_max_map_count.conf
sysctl --system

# Install docker-compose, cookiecutter and pipenv for the user
su -c "pip install --user cookiecutter pipenv docker-compose" $user

# Add "$HOME/.local/bin" to the user's PATH if not already done
grep -qF '# added by Invenio Bootcamp script' /home/$user/.bashrc || cat >> /home/$user/.bashrc <<EOF
export PATH=\$HOME/.local/bin:\$PATH  # added by Invenio Bootcamp script
EOF
grep -qF '# added by Invenio Bootcamp script' /home/$user/.bashrc || cat >> /home/$user/.profile <<EOF
export PATH=\$HOME/.local/bin:\$PATH  # added by Invenio Bootcamp script
EOF

# Install Chrome and ChromeDriver
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y install google-chrome-stable
wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -P /tmp/
unzip -d /tmp /tmp/chromedriver_linux64.zip
mv /tmp/chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
