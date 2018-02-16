# MarRef Bioschemas sample webpages

# Introduction
This is a demo project with some sample pages extract from the MarRef database ([https://mmp.sfb.uit.no/](https://mmp.sfb.uit.no/))
The idea behind this is to provide a sandbox where people can try to interact with MarRef samples using BioSchemas specification
This repo contains a copy of the [bsbang-crawler](https://github.com/justinccdev/bsbang-crawler) modified for the demo pourposes

# Docker
In order to make this work you need to have [Docker](https://www.docker.com/community-edition) installed and [Docker Compose ](https://docs.docker.com/compose/install/#prerequisites)

# Containers
There are multiple containers in this project to separate the different services
- *mar-ref*: aims to serve some static pages from the MarRef database
- *solr*: aims to store and index the bioschemas the crawler was able to extract


# Run all the containers
To run the containers, just lunch the `serve.sh` script
```bash
./serve.sh
```

You should be able (once the container is up) to check the MarRef static pages [here](http://localhost:8080/) and solr [here](http://localhost:8983)

# Stop all the containers
To stop all the containers, just lunch `stop.sh` script
```bash
./stop.sh
```

# Start/stop single containers
If you don't need all the containers at the same time, or you need to stop only one of the containers, you can use directly `docker-compose` syntax.
```bash
# Start mar-ref
docker-compose up -d mar-ref

# Stop mar-ref
docker-compose down mar-ref
```

