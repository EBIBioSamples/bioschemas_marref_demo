#!/bin/bash

docker run -d --name mar-ref -p 8080:8080 -v $(pwd)/src:/MarRef mar-ref 
