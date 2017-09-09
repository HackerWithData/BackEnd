## Setup Vagrant Environment

```
    # Install VirtualBox from: www.virtualbox.org/wiki/Downloads
    # Install Vagrant from: www.vagrantup.com/downloads.html

    git clone https://github.com/Banana-Mango/Backend.git
    cd Backend/
    vagrant box add ubuntu/xenial64

    # boot Vagrant environment
    vagrant up

    # ssh Virtual Machine
    vagrant ssh
```
Vagrant will synchronize Backend/ to the /vagrant directory
in vm, and it forwards the port 8888 of vm to host's 8888.

## Install
Install dependencies for project in virtual environment
```
    # ssh into virtual machine
    vagrant ssh

    # Next steps are all in vm
    cd /vagrant

    # Setup a virtualenv and active
    virtualenv env
    . env/bin/activate

    # Set configuration to be development
    export DJANGO_SETTINGS_MODULE="backend_core.settings.dev"
    
    make bootstrap  	# install dependencies

```

## Activate Virtual Environment
Activate the environment before doing anything else because all the
dependencies are installed in environment
```
    . env/bin/activate
```

## Install new packages, Skip if no new packages need to be installed
```
    pip install [package]
    pip freeze > requirements.txt
```

## Connect to MySQL
```
    mysql -h localhost -P 3306 -u root -p
    # default password: development
```

## Connect to Solr
```
    #check Solr connection status
    service solr status
```