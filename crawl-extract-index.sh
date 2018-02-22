#!/bin/bash
docker-compose up bsbc-crawl

docker-compose up bsbc-extract

docker-compose up bsbc-index
