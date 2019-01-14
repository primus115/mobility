FROM ubuntu:18.04

MAINTAINER Primoz Zajec (za.primoz@gmail.com)
LABEL Description="Dockerised SUMO, python DApp and react.js DApp for Mobi Challenge"

ENV MOBI_USER mobi

# Add a separate ppa with up-to-date SUMO version
RUN apt-get update
RUN apt-get -qq install software-properties-common
RUN add-apt-repository ppa:sumo/stable
RUN apt-get -qq install curl
#RUN curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh


# Install system dependencies.
RUN apt-get update && apt-get -qq install \
    wget \
    git \
    build-essential \
	sumo \
	sumo-tools \
	sumo-doc

# add user
RUN adduser $MOBI_USER --disabled-password
# install nodejs version v10
RUN cd /home/$MOBI_USER && curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh \
&& bash nodesource_setup.sh && apt-get -qq install nodejs

# Clone mobility repository
RUN cd /home/$MOBI_USER && git clone https://primus115@bitbucket.org/primus115/mobi.git

# Go to web folder and install dependencies
RUN cd /home/$MOBI_USER/mobi/web/mqttMaps/ && npm install

# python 3
RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# python dependencies
RUN pip install paho-mqtt
RUN pip3 install web3

# for finding sumo modules
ENV SUMO_HOME=/usr/share/sumo/

WORKDIR /home/$MOBI_USER/mobi/

EXPOSE 3000
