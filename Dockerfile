FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>
# This container runs the web layer of Brimstone 3
# Brimstone is a an application to manage construction jobs

# Port to access the Flask application on - change if needed.
EXPOSE 80

# RUN apt-get update ;\
#     apt-get -y upgrade

####################
# PYTHON and TOOLS #
####################
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-pip python-dev
RUN DEBIAN_FRONTEND=noninteractive pip install flask requests

############
# Development only tools, could be removed later
############
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install vim

#################
# App install 
#################
RUN mkdir -p /usr/local/brimstone/static
RUN mkdir -p /usr/local/brimstone/templates

# Executable -----------------
ADD dlt_web.py /usr/local/brimstone/
ADD static /usr/local/brimstone/static
ADD templates /usr/local/brimstone/templates

#################
# App Options 
#################
# Place bash users directly into /usr/local/brimstone
WORKDIR /usr/local/brimstone

# By default when this container runs, simply start the application
# CMD /usr/local/brimstone/dlt_web.py
CMD /usr/local/brimstone/dlt_web.py
