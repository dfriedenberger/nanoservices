FROM python:3

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        locales locales-all
        
# set timezone to Europ/Berlin
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN pip3 install --upgrade pip

