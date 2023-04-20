# Invoicy-backend

## Creating a virtual environment
To create a virtual environment, run the following commands:

    python3 -m venv venv
    source venv/bin/activate

## Installing dependencies
To install dependencies, run the following command:

    pip install -r requirements.txt

## Setting up MySQL client

Create a new database in MySQL.

### Connecting to MySQL
To connect to MySQL, run the following command:

    mysql -u root -p

### Creating a new database
To create a new database, run the following command:

    CREATE DATABASE <name>;


## Updating the environment variables
To update the environment, run the following commands:

    cd invoicy
    cp .env.example .env

Update the fields in .env file as follows:

    DATABASE_NAME=<db-name>
    DATABASE_USER=<db-user>
    DATABASE_PASS=<db-password>

## Migrating the Database
To migrate the database, run the following commands:

    python manage.py makemigrations
    python manage.py migrate

## Starting the server
To start the server, run the following command:

    python manage.py runserver