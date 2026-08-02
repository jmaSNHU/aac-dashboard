# import_data.py
# driver script for creating the aac database
# and import data from the AAC dataset
#
# Jacob Ard
# SNHU CS-499 Capstone
# Enhancement: Databases
# Script use
# August 1, 2026

# import the AacDataImporter class
from sqlite_data_import import AacDataImporter

# drop aac database tables if exists,
# create aac database,
# import aac dataset and create relational subtables
importer = AacDataImporter("aac.db", "aac_shelter_outcomes.csv")
importer.import_data()
