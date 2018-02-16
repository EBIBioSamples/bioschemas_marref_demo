#!/bin/bash

# Build the docker images
docker-compose build

# Run the services
docker-compose up -d mar-ref-solr mar-ref-site

