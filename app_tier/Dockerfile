FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>
# This container runs the application layer of Brimstone 3
# Brimstone is a an application to manage construction jobs

# Port to access the Flask application on - change if needed.
EXPOSE 5000

RUN apt-get update ;\
    apt-get -y upgrade

####################
# PYTHON and TOOLS #
####################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip python-dev libmysqlclient-dev
RUN DEBIAN_FRONTEND=noninteractive pip install flask requests
RUN pip install MySQL-python

#################
# GIT and MYSQL #
#################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git mysql-client

############
# Development only tools - remove before runtime
############
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install vim

#################
# App Install   #
#################
CMD mkdir /usr/local/brimstone
# Executable -----------------
ADD dlt_app.py /usr/local/brimstone/

#################
# App Options
#################
# Place bash users directly into /usr/local/brimstone
WORKDIR /usr/local/brimstone

# By default when this container runs, simply start the application
CMD /usr/local/brimstone/dlt_app.py
