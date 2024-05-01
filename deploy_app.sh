#!/bin/bash

DATABASE_ADDRESS=$1
DATABASE_PORT=$2
DATABASE_USER=$3
DATABASE_PASSWORD=$4
APP_PORT=$5

sudo apt-get update
sudo apt-get install -y git

git clone https://oauth2:glpat-8QYQLvwzP_wgjNqecANb@gitlab-stud.elka.pw.edu.pl/piar_student_projects/24l/z10.git
cd z10

# Pobieranie najnowszej wersji Docker'a
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Aktualizacja pliku konfiguracyjnego bazy danych
sed -i "s/postgres_db/$DATABASE_ADDRESS/" app/config.py

# Budowanie obrazu z Dockerfile
sudo docker build -t myflaskapp .

# Uruchomienie kontenera Docker
sudo docker run -d --name myflaskapp -p $APP_PORT:5000 \
-e DB_USER=$DATABASE_USER \
-e DB_PASSWORD=$DATABASE_PASSWORD \
-e DB_NAME=app_db \
-e DB_HOST=$DATABASE_ADDRESS \
-e FLASK_ENV=DEV \
-e DB_PORT=$DATABASE_PORT \
myflaskapp
