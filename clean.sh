#!/bin/bash
set -e

echo "Cleaning crawler database"
rm -f data/crawler/crawl.db


echo "Cleaning solr"
rm -fr data/solr/bsbang
