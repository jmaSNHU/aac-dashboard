# sqlite_create_tables.py
# python script to DROP and CREATE
# sqlite tables for the aac database
#
# Run this script to initialize the SQLite database
# for the AAC outcomes dashboar
#
# Jacob Ard
# SNHU CS-499 Capstone
# Enhancement: Databases
# July 28, 2026


# import sqlite3 module
import sqlite3



# drop tables 
def drop_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS animal")
    cursor.execute("DROP TABLE IF EXISTS animal_type")
    cursor.execute("DROP TABLE IF EXISTS breed")
    cursor.execute("DROP TABLE IF EXISTS outcome_type")
    cursor.execute("DROP TABLE IF EXISTS sex_upon_outcome")

# create the animals table
# foreign key columns: animal_type_id, breed_id, outcome_type_id, sex_upon_outcome_id
def create_animal_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age_upon_outcome TEXT,
            animal_id TEXT,
            animal_type_id INTEGER,
            breed_id INTEGER,
            color TEXT,
            date_of_birth TEXT,
            datetime TEXT,
            month_year TEXT,
            name TEXT,
            outcome_subtype TEXT,
            outcome_type_id INTEGER, 
            sex_upon_outcome_id INTEGER,
            location_lat NUMERIC,
            location_long NUMERIC,
            age_upon_outcome_in_weeks NUMERIC
            )        
    ''')

# create the animal_type table
def create_animal_type_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS animal_type(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_type TEXT
        )        
    ''')

# create the breed table
def create_breed_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS breed(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_name TEXT
        )
    ''')

# create the outcome_type table
def create_outcome_type_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS outcome_type(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome_type TEXT
        ) 
    ''')

# create the sex_upon_outcome table
def create_sex_upon_outcome_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS sex_upon_outcome(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sex TEXT
        )
    ''')

def drop_and_create_tables():
    # create a connection
    # will create database file if it does not exist
    connection = sqlite3.connect("test.db")

    cursor = connection.cursor()

    drop_tables(cursor)
    create_animal_table(cursor)
    create_animal_type_table(cursor)
    create_breed_table(cursor)
    create_outcome_type_table(cursor)
    create_sex_upon_outcome_table(cursor)

    # commit transactions and create all tables
    connection.commit()

    connection.close()
