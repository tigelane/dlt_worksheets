#!/bin/bash

WEB="dlt_web"
APP="dlt_app"
DB="dlt_db"
jenkins="dlt_jenkins"

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

function build_containers() {
    CACHE=$1
    # Build the containers either normal or cached
    ####  Web Tier
    cd /Users/tige/Documents/Development/dlt_worksheets
    docker build $CACHE -t tigelane/brimstone_web .
    ####  App Tier
    cd /Users/tige/Documents/Development/dlt_worksheets/app_tier
    docker build $CACHE -t tigelane/brimstone_app .
}

function not_used() {
    WEB="dlt_web"
    IPADDRESS="192.168.55.115"
    docker stop $WEB
    docker run --rm --name $WEB -v /Users/tige/Documents/Development/dlt_worksheets:/opt/brimstone -e APP_SERVER_IPADDR=$IPADDRESS -p 80:80 -ti tigelane/brimstone_web bash

    APP="dlt_app"
    IPADDRESS="192.168.55.115"
    docker stop $APP
    docker run --rm --name $APP -v /Users/tige/Documents/Development/dlt_worksheets/app_tier:/opt/brimstone -e SQL_SERVER_IPADDR=$IPADDRESS -p 5000:5000 -ti tigelane/brimstone_app bash

    docker run --rm --name $JENKINS -p 8080:8080 -p 50000:50000 -v /Users/tige/Documents/Development/Jenkins:/var/jenkins_home jenkins
}
# Start all of the containers
function start_containers() {
    # Stop the containers if they are already running
    stop
    
    # Run
    printf "\n\nStarting containers:\n"
    docker run --rm --name $WEB -v /Users/tige/Documents/Development/dlt_worksheets:/opt/brimstone -e APP_SERVER_IPADDR=$IPADDRESS -p 80:80 -d tigelane/brimstone_web /opt/brimstone/$WEB.py

    docker run --rm --name $APP -v /Users/tige/Documents/Development/dlt_worksheets/app_tier:/opt/brimstone -e SQL_SERVER_IPADDR=$IPADDRESS -p 5000:5000 -d tigelane/brimstone_app /opt/brimstone/$APP.py

    #### Run the DB
    docker run --rm --name $DB -e MYSQL_ROOT_PASSWORD=H2xE6h6Bo9cgsnkiUhW076Qf -v /Users/tige/Documents/Development/dlt_worksheets/mysql:/var/lib/mysql -p 3306:3306 -d mysql

    #### Print some info
    printf "\n\nRunning containers:\n"
    docker ps --format 'table {{.Names}}\t{{.Image}}'
    printf "\n"
}

# Stop all running containers
function stop()
{
    printf "\n\nAttempting to stop containers:\n"
    docker stop $WEB $APP $DB

    printf "\nContainers still running:\n"
    docker ps --format 'table {{.Names}}\t{{.Image}}'
    printf "\n"
}

# Extract options and their arguments into variables.
while getopts "cbhrsi:" opt; do
  case $opt in
    c)
        CACHE="--no-cache"
        ;;
    b)
        build_containers $CACHE
        ;;
    h) 
        usage
        exit 1 
        ;;
    i)
        IPADDRESS=$OPTARG >&2
        ;;
    r)
        start_containers
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


