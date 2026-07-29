# python script to DROP and CREATE 
# sqlite tables for the aac database
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

# commit transactions and create all tables
connection.commit()

connection.close()
