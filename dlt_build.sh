#!/bin/bash

cd /Users/tige/Documents/Development/dlt_worksheets
docker build -t tigelane/brimstone_web .

docker run -v /Users/tige/Documents/Development/dlt_worksheets:/usr/local/brimstone -e APP_SERVER_IPADDR=192.168.55.115 -p 80:80 -d tigelane/brimstone_web


cd /Users/tige/Documents/Development/dlt_worksheets/app_tier
docker build -t tigelane/brimstone_app .

docker run -v /Users/tige/Documents/Development/dlt_worksheets/app_tier:/usr/local/brimstone -e SQL_SERVER_IPADDR=192.168.55.115 -p 5000:5000 -d tigelane/brimstone_app

echo "Running containers:"
docker ps -n 2 -q
