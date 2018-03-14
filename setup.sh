#!/bin/bash
set -e
echo "Cleaning existing volumes"
#remove any images, in case of out-of-date or corrupt images
docker-compose down --volumes --rmi local --remove-orphans
./clean.sh

# Build the docker images
echo "Building docker images"
docker-compose build

# Run the services
docker-compose up -d mar-ref-solr mar-ref-site
echo "Wait 30 sec for solr to be up"
sleep 30

# Run the setup of the crawler
echo "Setting up the env for the crawler"
docker-compose up bsbc-setup

