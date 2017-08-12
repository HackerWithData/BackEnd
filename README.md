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