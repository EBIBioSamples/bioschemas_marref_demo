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


# Run the containers
To run the containers, just lunch the `serve.sh` script
```bash
./serve.sh
```

# Stop the containers
To stop all the containers, just lunch `stop.sh` script
```bash
./stop.sh
```



