#!/bin/bash
clean=0
while [ "$1" != "" ]; do
    case $1 in
        -c | --clean )    		clean=1
                                ;;
    esac
    shift
done

#cleanup any previous data
if [ $clean == 1 ]
then
	echo "Cleaning existing volumes"
	#remove any images, in case of out-of-date or corrupt images
	docker-compose down --volumes --rmi local --remove-orphans

	./clean.sh
else
	docker-compose down --remove-orphans
fi
set -e

# Build the docker images
docker-compose build

# Run the services
docker-compose up -d mar-ref-solr mar-ref-site
echo "Wait 30 sec for solr to be up"
sleep 30

# Run the setup of the crawler
docker-compose up bsbc-setup

