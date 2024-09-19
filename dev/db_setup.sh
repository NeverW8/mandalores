#!/bin/bash

DB_USER="psql"
DB_PASSWORD="password"
DB_NAME="mandalores_db"

sudo -u postgres psql <<EOF
-- Create a new PostgreSQL user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Create a new PostgreSQL database
CREATE DATABASE $DB_NAME;

-- Grant all privileges on the new database to the new user
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Connect to the new database and grant privileges on the public schema
\c $DB_NAME
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;

-- Exit the PostgreSQL prompt
\q
EOF

echo "PostgreSQL user '$DB_USER', database '$DB_NAME', and privileges setup completed."

