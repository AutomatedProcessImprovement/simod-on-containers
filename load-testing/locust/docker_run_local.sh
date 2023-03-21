#!/usr/bin/env bash

docker run --rm -it -p 8089:8089 -v $(pwd)/locustfile.py:/home/locust/locustfile.py nokal/simod-http-locust:1.0.0