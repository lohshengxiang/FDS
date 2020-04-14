# Setup Guide

##Python Setup

Ensure Python 3 is installed with the following packages:

Flask, flask-Login, flask-wtf, cryptography, datetime



##Postgresql Setup

In the views.py file, locate the line 

conn = psycopg2.connect("dbname=fds2 user=postgres host = localhost password = password")

and replace the password (and user if required) parameter with your psql password.



Create a database in psql called ‘fds2’ by entering the following in the psql terminal:

create database fds2;

\c fds2



After connecting to the database, travel to the work directory containing the postgres.sql file. Initiate the following files:

\i postgres.sql

\i UDF.sql



## Execution

Execute the program using your windows terminal by traveling to the directory containing the main.py file. Execute using the following command:

python main.py



Afterwhich, the following will appear on the terminal:

 \* Serving Flask app "main" (lazy loading)

 \* Environment: production

  WARNING: Do not use the development server in a production environment.

  Use a production WSGI server instead.

 \* Debug mode: on

INFO:werkzeug: * Running on http://localhost:5000/ (Press CTRL+C to quit)



On the internet browser, go to http://localhost:5000/ to start the webapp. 