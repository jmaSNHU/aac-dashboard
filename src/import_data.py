from sqlite_data_import import AacDataImporter


importer = AacDataImporter("test.db", "aac_shelter_outcomes.csv")
importer.create_database()
importer.import_data()
