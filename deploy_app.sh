#!/bin/bash

DATABASE_ADDRESS=$1
DATABASE_PORT=$2
DATABASE_USER=$3
DATABASE_PASSWORD=$4
APP_PORT=$5

GIT_REPO="https://github.com/yourusername/yourapp.git"
GIT_TOKEN="app_token" 

sudo apt-get update
sudo apt-get install -y git

git clone https://<token>:x-oauth-basic@${GIT_REPO#"https://"}
cd Z10

# Pobieranie najnowszej wersji Docker'a
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Budowanie obrazu z Dockerfile
sudo docker build -t myflaskapp .

# Uruchomienie kontenera Docker
sudo docker run -d --name myflaskapp -p $APP_PORT:5000 \
-e DB_USER=$DATABASE_USER \
-e DB_PASSWORD=$DATABASE_PASSWORD \
-e DB_NAME=app_db \
-e DB_HOST=$DATABASE_ADDRESS \
-e FLASK_ENV=DEV
-e DB_PORT=$DATABASE_PORT \
myflaskapp
