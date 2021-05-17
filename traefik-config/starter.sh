#!/bin/bash

USERNAME=$1
PASSWORD=$2
ACME_MAIL="YOURMAIL"
YOUR_DOMAIN="monitor.domain.com"

DOCKER=$(which docker)
DOCKER_COMPOSE=$(which docker-compose)
STATIC_FILE="$(pwd)/traefik.toml"
DYNAMIC_FILE="$(pwd)/traefik_dynamic.toml"
LOG_DIR="/var/log/traefik"

echo "-------------- INSTALLING DEPENDENCIES --------------"
touch acme.json
chmod 600 acme.json
sudo curl -fsSL https://get.docker.com | bash
sudo apt install apache2-utils docker-compose

echo "-------------- CREATING DOCKER NETWORK WEB --------------"

$DOCKER network create web

echo "-------------- CREATING CREDENTIALS FOR MONITORING WEBSITE --------------"

CREDENTIALS=$($(which htpasswd) -nb $USERNAME $PASSWORD | cut -d " " -f 3)

sed -i -e "s/PLEASEREPLACEME/"$CREDENTIALS"/g" $DYNAMIC_FILE
sed -i -e "s/YOURDOMAIN/"$YOUR_DOMAIN"/g" $DYNAMIC_FILE
sed -i -e "s/PLEASEREPLACEMAIL/\\$ACME_MAIL/g" $STATIC_FILE

echo "-------------- PREPARING NOW TRAEFIK CONTAINER --------------"

mkdir -p $LOG_DIR
$DOCKER_COMPOSE up -d

echo "-------------- FINISHED --------------"
