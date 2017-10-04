#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "Provision Start"
apt-get update

echo "Installing libmagickwand-dev"
apt-get install libmagickwand-dev -y > /dev/null

echo "Installing virtualenv"
#including pip, setuptools
apt-get install python-virtualenv -y > /dev/null

echo "Installing python-dev"
apt-get install python-dev -y > /dev/null

echo "Preparing MySQL"
apt-get install debconf-utils -y > /dev/null

install MySQL
apt-get install libmysqlclient-dev > /dev/null
debconf-set-selections <<< "mysql-server mysql-server/root_password password development"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password development"
echo "Installing MySQL"
apt-get install mysql-server -y > /dev/null

echo "Installing JDK8"
apt-get install default-jre -y > /dev/null

echo "Installing solr-tomcat"
apt-get install solr-tomcat


#cd /tmp
#curl -O http://apache.mirrors.lucidnetworks.net/lucene/solr/6.6.0/solr-6.6.0.tgz
#tar xzf solr-6.6.0.tgz
#solr-6.6.0/bin/install_solr_service.sh solr-6.6.0.tgz


apt-get install git -y > /dev/null

echo "Provision End"