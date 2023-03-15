#!/usr/bin/env bash

docker run --rm -it -p 8089:8089 -v $(pwd)/locustfile.py:/home/locust/locustfile.py nokal/locust:2.15.1