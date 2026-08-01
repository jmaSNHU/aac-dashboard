# python script to DROP and CREATE 
# sqlite tables for the aac database
#
# Run this script to initialize the SQLite database
# for the AAC outcomes dashboar
#
# Jacob Ard
# SNHU CS-499 Capstone
# Enhancement: Databases


# import sqlite3 module
import sqlite3


# create a connection
# will create database file if it does not exist
connection = sqlite3.connect("test.db")

cursor = connection.cursor()

# drop tables 
cursor.execute("DROP TABLE IF EXISTS animals")
cursor.execute("DROP TABLE IF EXISTS animal_type")
cursor.execute("DROP TABLE IF EXISTS breed")
cursor.execute("DROP TABLE IF EXISTS outcome_type")
cursor.execute("DROP TABLE IF EXISTS sex_upon_outcome")

# create the animals table
# normalized columns: animal_type, breed, outcome_type, sex_upon_outcome
cursor.execute(
        '''CREATE TABLE IF NOT EXISTS animals (
            rec_num INTEGER PRIMARY KEY AUTOINCREMENT,
            age_upon_outcome TEXT,
            animal_id TEXT,
            animal_type_id INTEGER,
            breed_id INTEGER,
            color TEXT,
            date_of_birth TEXT,
            datetime TEXT,
            monthyear TEXT,
            name TEXT,
            outcome_subtype TEXT,
            outcome_type_id INTEGER, 
            sex_upon_outcome_id INTEGER,
            location_lat NUMERIC,
            location_long NUMERIC,
            age_upon_outcome_in_weeks NUMERIC
            )        
''')

cursor.execute(
        '''CREATE TABLE IF NOT EXISTS animal_type(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT
        )        
''')

cursor.execute(
        '''CREATE TABLE IF NOT EXISTS breed(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_name TEXT
        )
''')

cursor.execute(
        '''CREATE TABLE IF NOT EXISTS outcome_type(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outcome_type TEXT
        ) 
''')

cursor.execute(
        '''CREATE TABLE IF NOT EXISTS sex_upon_outcome(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sex TEXT
        )
''')

# commit transactions and create all tables
connection.commit()

connection.close()
