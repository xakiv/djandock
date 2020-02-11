FROM python:3.8-buster
MAINTAINER ChakibBHB <niark.hipps@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
# RUN mkdir /code WORKDIR already create /code dir if it doesn't exist
WORKDIR /code

# Dépendances systemes pour le projet
RUN apt-get update
RUN apt-get install -y python3-dev

# Ubuntugis
# RUN apt-get install -y build-essential software-properties-common
# RUN echo "deb http://ppa.launchpad.net/ubuntugis/ubuntugis-unstable/ubuntu bionic main " >> /etc/apt/sources.list
# RUN echo "deb-src http://ppa.launchpad.net/ubuntugis/ubuntugis-unstable/ubuntu bionic main " >> /etc/apt/sources.list
# RUN add-apt-repository ppa:ubuntugis/ppa
# ---unstable--- pour ubuntu18.04
# RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable
# RUN apt-get update
# RUN apt-get upgrade -y

RUN apt-get install -y libxml2-dev libjson-c-dev libgdal-dev libproj-dev libgeos-dev binutils gdal-bin python-psycopg2 postgis
# RUN apt-get install -y postgis postgresql-11-postgis-2.5 postgresql-11-postgis-2.5-scripts python-psycopg2
RUN apt-get install -y vim htop

RUN apt-get update

# Dépendances python pour nos applications
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# SID django app data ajouté au container web
RUN django-admin startproject config .
COPY config/ ./config/
COPY data/ ./data/
COPY .env ./
COPY sid/ ./sid
COPY map_quest/ ./map_quest

# Scripts pour séquence de deploiement
COPY entrypoints/wait_for_postgres.py ./wait_for_postgres.py
RUN chmod +x ./wait_for_postgres.py
COPY entrypoints/start.sh ./start.sh
RUN chmod +x ./start.sh

EXPOSE 8000
