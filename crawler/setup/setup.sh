#!/bin/bash
set -e

echo "Clear the sqlite database"
touch /crawler/data/crawl.db

echo "Initialize the sqlite database"
python bsbang-setup-sqlite.py

echo "Initialize solr"
python bsbang-setup-solr.py ../conf/bsbang-solr-setup.xml

echo "Finished"
