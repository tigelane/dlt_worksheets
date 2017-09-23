#!/bin/bash

WEB="dlt_web"
APP="dlt_app"
DB="dlt_db"

CLEANB=0
CACHE=""
BUILD=0
RUN=0
IPADDRESS="192.168.55.115"

function usage()
{
echo "How to use:"  $0
echo
echo "-b            Build containers"
echo "-c            Build containers with no cache"
echo "-h            Help"
echo "-i IPADDRESS  IP Address to use for servers"
echo "-r            run or start the application"
echo "-s            Stop all containers"
echo ""
}

function stop()
{
    printf "\n\nAttempting to stop containers:\n"
    docker stop $WEB $APP $DB

    printf "\nContainers still running:\n"
    docker ps --format 'table {{.Names}}\t{{.Image}}'
    printf "\n"
}

# Extract options and their arguments into variables.
while getopts "bchrsi:" opt; do
  case $opt in
    b)
        BUILD=1
        ;;
    c)
        CLEANB=1
        ;;
    h) 
        usage
        exit 1 
        ;;
    i)
        echo "i Triggered $OPTARG" >&2
        IPADDRESS=$OPTARG >&2
        echo IP Address is: $IPADDRESS
        ;;
    r)
        RUN=1
        ;;
    s) 
        stop
        exit 0 
        ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    esac
done

# echo CLEANB is: "${CLEANB}"
# echo IP Address is: "${IPADDRESS}"

# Fresh build or cached
if [ $CLEANB -eq 1 ]
then
    CACHE="--no-cache"  
fi

# Build the containers either normal or cached
if [ $BUILD -eq 1 ]
then
    ####  Web Tier
    cd /Users/tige/Documents/Development/dlt_worksheets
    docker build $CACHE -t tigelane/brimstone_web .
    ####  App Tier
    cd /Users/tige/Documents/Development/dlt_worksheets/app_tier
    docker build $CACHE -t tigelane/brimstone_app .
fi

# Start all of the containers
if [ $RUN -eq 1 ]
then
    # Stop the containers if they are already running
    stop
    # Run
    printf "\n\nStarting containers:\n"
    docker run --rm --name $WEB -v /Users/tige/Documents/Development/dlt_worksheets:/opt/brimstone -e APP_SERVER_IPADDR=$IPADDRESS -p 80:80 -d tigelane/brimstone_web
    # docker run  -e APP_SERVER_IPADDR=192.168.55.115 -p 80:80 -d tigelane/brimstone_web

    docker run --rm --name $APP -v /Users/tige/Documents/Development/dlt_worksheets/app_tier:/usr/local/brimstone -e SQL_SERVER_IPADDR=$IPADDRESS -p 5000:5000 -d tigelane/brimstone_app

    #### Run the DB
    docker run --rm --name $DB -e MYSQL_ROOT_PASSWORD=H2xE6h6Bo9cgsnkiUhW076Qf -v /Users/tige/Documents/Development/dlt_worksheets/mysql:/var/lib/mysql -p 3306:3306 -d mysql

    #### Print some info
    printf "\n\nRunning containers:\n"
    docker ps --format 'table {{.Names}}\t{{.Image}}'
    printf "\n"
fi
