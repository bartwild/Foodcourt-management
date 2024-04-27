#!/bin/bash

DATABASE_PORT=$1
DATABASE_USER=$2
DATABASE_PASSWORD=$3

# Instalacja PostgreSQL
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Konfiguracja PostgreSQL do akceptowania połączeń sieciowych
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/12/main/postgresql.conf
sudo sed -i "s/#port = 5432/port = $DATABASE_PORT/" /etc/postgresql/12/main/postgresql.conf

# Konfiguracja reguł dostępu
echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/12/main/pg_hba.conf

# Restart PostgreSQL
sudo systemctl restart postgresql

# Ustawienie użytkownika i hasła
sudo -u postgres psql -c "CREATE USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE app_db OWNER $DATABASE_USER;"
