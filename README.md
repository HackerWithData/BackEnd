## Setup Vagrant Environment

```
    # Install VirtualBox from: www.virtualbox.org/wiki/Downloads
    # Install Vagrant from: www.vagrantup.com/downloads.html

    git clone https://github.com/Banana-Mango/Backend.git
    cd Backend/
    vagrant box add ubuntu/trusty64

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

    make bootstrap  	# install dependencies
    make bootstrap_db   # create database and tables
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

## DB Migration, not completed
```
    # upgrade
    alembic revision -m "REVISION NAME"
    # modify revision file in alembic/version/
    make upgrade_db

    #downgrade
    make downgrade_db
```