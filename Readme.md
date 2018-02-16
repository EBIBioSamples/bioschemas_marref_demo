# MarRef Bioschemas sample webpages

# Introduction
This is a demo project with some sample pages extract from the MarRef database ([https://mmp.sfb.uit.no/](https://mmp.sfb.uit.no/))
The idea behind this is to provide a sandbox where people can try to interact with MarRef samples using BioSchemas specification
This repo contains a copy of the [bsbang-crawler](https://github.com/justinccdev/bsbang-crawler) modified for the demo pourposes

# Docker
In order to make this work you need to have [Docker](https://www.docker.com/community-edition) installed and [Docker Compose ](https://docs.docker.com/compose/install/#prerequisites)

## Notes for Docker on Linux
Check out this [notes](https://docs.docker.com/install/linux/linux-postinstall/) after you have installed Docker if you're on Linux

# Containers
There are multiple containers in this project to separate the different services
- *mar-ref-site*: aims to serve some static pages from the MarRef database
- *mar-ref-solr*: aims to store and index the bioschemas the crawler was able to extract
- *bsbang-crawler*: container with all the crawler functionalities
- *bsbc-setup*: container to setup solr and sqlite for the crawler to work
- *bsbc-crawl*: container to crawl the provided sitemap
- *bsbc-extract*: container to extract the jsonld from webpages stored from crawl
- *bsbc-index*: container to index the results in solr

# Run all the containers
To run the containers, just lunch the `serve.sh` script
```bash
./setup.sh
```

You should be able (once the container is up) to check the MarRef static pages [here](http://localhost:8080/) and solr [here](http://localhost:8983)

# Run the crawler
In order to run the crawler, you need to run one after the other the various containters using docker-compose sintax.
```bash
# Crawling
docker-compose up bsbc-crawl

# Extracting
docker-compose up bsbc-extract

# Indexing
docker-compose up bsbc-index
```

With the last operation, you should be able to find all your data in the solr index [webpage](http://localhost:8983/)

# Stop all the containers
To stop all the containers, just lunch `stop.sh` script
```bash
./stop.sh
```

# Start/stop single containers
If you don't need all the containers at the same time, or you need to stop only one of the containers, you can use directly `docker-compose` syntax, e.g.
```bash
# Start mar-ref-site
docker-compose up -d mar-ref-site

# Stop mar-ref
docker-compose down mar-ref-site
```

# NOTE
Could be that some of the commands will not work directly, try to stick a `sudo` in front of the command
