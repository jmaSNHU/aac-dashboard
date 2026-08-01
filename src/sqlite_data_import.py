# python script to DROP and CREATE 
# sqlite tables for the aac database
#
# Jacob Ard
# SNHU CS-499 Capstone
# Enhancement: Databases


# import sqlite3 module
import csv
import sqlite3
import sqlite_create_tables


class AacDataImporter:
    # constructor
    def __init__(self, db, csv_file):
        # cache related records locally for faster access
        self.animal_type_cache = {}
        self.breed_cache = {}
        self.outcome_type_cache = {}
        self.sex_upon_outcome_cache = {}

        # open sqlite connection and create cursor object
        # the logic is to wrap the entire process in a single
        # transaction and rollback if the import fails
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor() 

        # enable foreign keys
        self.cursor.execute("PRAGMA foreign_keys=ON;")

        self.csv_file = csv_file

    # call script to drop and create sqlite tables
    def create_database(self):
        sqlite_create_tables.drop_and_create_tables()

    def get_or_insert_relation(self, table, column, value, cache):
        if not value:
            return None
        # trim whitespace
        value = value.strip()

        if value in cache:
            # return the foreign key id
            return cache[value]

        # insert {value} into {table} 
        self.cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
        # select the newly created ID 
        self.cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value, ))

        # get the id from the cursor
        foreign_key = self.cursor.fetchone()[0]

        # cache the id using value as the dict key
        cache[value] = foreign_key

        return foreign_key

    def import_data(self):
        # open csv file for reading, will close after with block
        with open(self.csv_file, mode="r", encoding="UTF-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # strip whitespace from all values in the row
                row = {col: val.strip() for col, val in row.items()}
                
                # query or create animal_type and get ID
                animal_type_id = self.get_or_insert_relation(
                        "animal_type",
                        "type", 
                        row["animal_type"], 
                        self.animal_type_cache)

                # query or create breed and get ID
                breed_id = self.get_or_insert_relation(
                        "breed",
                        "breed_name",
                        row["breed"],
                        self.breed_cache)
                # query or create outcome_type and get ID
                outcome_type_id = self.get_or_insert_relation(
                        "outcome_type",
                        "outcome_type",
                        row["outcome_type"],
                        self.outcome_type_cache)
                # query or create sex_upon_outcome and get ID
                sex_upon_outcome_id = self.get_or_insert_relation(
                        "sex_upon_outcome",
                        "sex",
                        row["sex_upon_outcome"],
                        self.sex_upon_outcome_cache)

                # insert row into the animal table
                self.cursor.execute("""
                    INSERT INTO animal(
                        rec_num, age_upon_outcome, animal_id, animal_type_id,
                        breed_id, color, date_of_birth, datetime, monthyear,
                        name, outcome_subtype, outcome_type_id, sex_upon_outcome_id,
                        location_lat, location_long, age_upon_outcome_in_weeks)

                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, ( row["rec_num"], row["age_upon_outcome"], row["animal_id"],
                          animal_type_id, breed_id, row["color"], row["date_of_birth"],
                          row["datetime"], row["monthyear"], row["name"], row["outcome_subtype"],
                          outcome_type_id, sex_upon_outcome_id, row["location_lat"], row["location_long"],
                          row["age_upon_outcome_in_weeks"]
                    ))
                
        self.connection.commit()
        self.connection.close()



