#! python3
''' 
    Purpose: This python code will be run when running the FITS Python app.  
    Essentially, the code in this file will check for the existence of MySQL,
    the MySQL database used for FITS issue tracking, and the table(s) used in 
    said DB. 

    If MySQL does exist, but he DB/table(s) do not, this script will attempt
    to initialize them
'''

import mysql.connector

dbs = {}
dbs['job_tracker_db'] = (
    "CREATE DATABASE job_tracker_db;"
)

tables = {}
tables['jobs_tbl'] = (
    "CREATE TABLE jobs_tbl(" +
    "  id INT(11) AUTO_INCREMENT PRIMARY KEY," +
    "  company VARCHAR(100)," +
    "  position VARCHAR(200)," +
    "  companyInfo TEXT," +
    "  positionInfo TEXT," +
    "  reqsIMeet TEXT," +
    "  reqsIDontMeet TEXT," +
    "  salary varchar(200)," +
    "  address VARCHAR(200)," +
    "  links TEXT," +
    "  status VARCHAR(200)," +
    "  rating INT," +
    "  rejected BOOLEAN," +
    "  username VARCHAR(30)," +
    "  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
)
tables['users'] = (
    "CREATE TABLE users(" +
    "  id INT(11) AUTO_INCREMENT PRIMARY KEY," +
    "  name VARCHAR(100)," +
    "  email VARCHAR(100)," +
    "  username VARCHAR(30)," +
    "  password VARCHAR(100)," +
    "  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
)


def checkAndMakeDB():
    db_connection = mysql.connector.connect(
        host="localhost",  # replace with wherever you host your db
        user="coltan",  # replace with your username
        password="qwerQWER1234!@#$"  # replace with a real password
    )
    db_cursor = db_connection.cursor()

    db_cursor.execute("SHOW DATABASES;")
    databases = [item[0] for item in db_cursor.fetchall()]

    for key in dbs:
        if key in databases:
            print("Found " + key + " database!")
        else:
            print("Database " + key + " not found. Creating new database...")
            db_cursor.execute(dbs[key])

    # If I ever used more than one DB for some reason, would need to update
    #  hard coded values here and in the for loop below...
    db_cursor.execute("SHOW TABLES in job_tracker_db;")

    dbTables = [item[0] for item in db_cursor.fetchall()]

    for key in tables:
        if key in dbTables:
            print("Found " + key + "!")
        else:
            print(key + " not found. Creating table...")
            db_cursor.execute("USE job_tracker_db;")
            db_cursor.execute(tables[key])

    db_cursor.close()
