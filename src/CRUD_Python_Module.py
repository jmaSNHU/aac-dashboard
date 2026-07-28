# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from pymongo import DESCENDING
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB""" 
    KEY_REC_NUM = "rec_num"

    # constructor with default argument values for the aac database
    def __init__(self, user, passwd, host, port, database, collection): 

        # Initializing the MongoClient to access the MongoDB 
        self.client = MongoClient("mongodb://%s:%s@%s:%d" % (user,passwd,host,port)) 
        self.database = self.client["%s" % (database)] 
        self.collection = self.database["%s" % (collection)] 

    # method to return the next available record number for use in the create method
    def get_next_record_number(self):
        """Returns the next rec_num value for the collection."""
        max_rec_num = self.database.animals.find_one(sort=[(self.KEY_REC_NUM, DESCENDING)])
        if max_rec_num is not None:
            return int(max_rec_num[self.KEY_REC_NUM]) + 1
        else:
            return 1; # no rec_num found
            
    # Create method. 
    # returns True after successful insert
    def create(self, data):
        """Accepts a dictionary argument and inserts a single document. 
        Returns true if insert is successful, otherwise false.
        """
        # verify that data is a dictionary and is not empty
        if isinstance(data, dict) and data:
            # add next record number if needed
            if self.KEY_REC_NUM not in data:
                data[self.KEY_REC_NUM] = self.get_next_record_number()
            
            # insert the document
            result = self.database.animals.insert_one(data)  # data should be dictionary
            # returns true if insertion successful
            return result.acknowledged
        else: 
            raise InvalidArgumentError(f"Create Failed. Invalid Data argument: {data}")

    # Read method 
    def read(self, filters=None):
        """Returns a list of documents from the animals collection. 
        Accepts optional filters argument. 
        Returns an empty list if no matching documents are found.
        """
        # find all documents that match query fields. Filters may be None or an empty dict.
        documents =  self.database.animals.find(filters) # filters is a dictionary 
        # will return empty list if no results are found
        return list(documents)
    
    # Update method
    def update(self, filters, data):
        """Updates records that match the required filters criteria. 
        Returns the number of updated documents.
        """
        # throw exception if filters is not a dict or is empty
        if not isinstance(filters, dict) or not filters:
            raise InvalidArgumentError(f"Update Failed. Invalid Filters argument: {filters}")
        # throw exception if data is not a dict or is empty
        elif not isinstance(data, dict) or not data:
            raise InvalidArgumentError(f"Update Failed. Invalid Data argument: {data}")
        else:
            # update all documents that match the provided filters with the specified data
            result = self.database.animals.update_many(filters, {"$set": data})
                
            # return the number of documents updated
            return result.modified_count
            
    # Delete method 
    def delete(self, filters):
        """Deletes records that match the required filters criteria. 
        Returns the number of deleted documents.
        """
        # verify that filters is a dict and is not empty
        if isinstance(filters, dict) and filters:
            # delete all documents that match the provided filters
            result = self.database.animals.delete_many(filters)
                
            # return the number of documents deleted
            return result.deleted_count
        else:
            raise InvalidArgumentError(f"Delete Failed. Invalid filters argument: {filters}")
            
            
# Custom Exception class for empty data parameter
# https://peps.python.org/pep-0008/#exception-names
class InvalidArgumentError(Exception):
    """Exception raised for missing CRUD method parameters."""
    
    # constructor takes a message and calls the base Exception constructor
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    # string representation
    def __str__(self):
        return f"InvalidParameterError: {self.message}"
