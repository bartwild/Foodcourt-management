#!/bin/bash

DATABASE_PORT=$1
DATABASE_USER=$2
DATABASE_PASSWORD=$3

# Instalacja potrzebnych narzędzi
sudo apt-get update
sudo apt-get install -y curl git

# Pobieranie najnowszej wersji Docker'a
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalacja Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Tworzenie pliku docker-compose.yml
cat << EOF > docker-compose.yml
version: '3.10'

services:
  postgres_db:
    image: postgres:latest
    container_name: PostgresCont
    restart: always
    environment:
      - POSTGRES_DB=app_db
      - POSTGRES_USER=$DATABASE_USER
      - POSTGRES_PASSWORD=$DATABASE_PASSWORD
    ports:
      - '$DATABASE_PORT:5432'
EOF

# Uruchomienie kontenera Docker
sudo docker-compose up -d
