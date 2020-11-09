# -*- mode: python -*-
# vi: set ft=python :

Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/xenial64'

  config.vm.network 'forwarded_port', guest: 5000, host: 5000
  config.vm.hostname = 'pladmed'
  config.vm.provider 'virtualbox' do |vb|
    vb.memory = '1024'
    vb.name = 'pladmed'
  end

  config.vm.provision 'shell', privileged: false, inline: <<-SHELL
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"

    sudo apt-get update
    sudo apt-get install -y build-essential git

    sudo apt-get install -y gnupg
    sudo wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
    sudo apt-get install -y binutils
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org

    sudo systemctl start mongod

    sudo apt-get install -y python3.6
    
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash

    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    nvm install node
    
    sudo apt-get -y install docker.io
    
    sudo apt install -y python-pip
    sudo apt install -y libpcap-dev libpq-dev
    pip install --upgrade pip
    pip install pipenv

    SHELL
end
