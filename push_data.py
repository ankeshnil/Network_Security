import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo  # is a Python library used to connect Python with MongoDB database.
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging 

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # here we get the mongodb env
print(MONGO_DB_URL) 

'''When Python connects to MongoDB Atlas, AWS, or any HTTPS API, it needs certificates to confirm the server is trusted.'''

import certifi   # is a Python library that provides a collection of trusted SSL certificates.
ca = certifi.where()   # Give me the path of the trusted certificate file so I can use it for secure connection


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkException(e, sys)
        
    def csv_to_json_conveter(self, file_path):
        data = pd.read_csv(file_path)
        data.reset_index(drop=True, inplace=True)
        record = list(json.loads(data.T.to_json()).values())
        return record 
    
    
    '''
    self → refers to the current class object
    record → the data you want to store in MongoDB
    database → the database name
    collection → the collection name (like a table)
    '''
    def insert_data_monfoDB(self, record, database, collection):
        try:
            self.record = record
            self.database = database
            self.collection = collection
            
            # Create a connection to MongoDB using the database URL and store that connection inside this class
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=ca
            )
            self.database = self.mongo_client[self.database] # Open the NetworkSecurity database.
            self.collection = self.database[self.collection] # Collections are like tables in SQL. and opne the collection
            
            self.collection.insert_many(self.record)
            return (len(self.record))
            
            
        except Exception as e:
            raise NetworkException(e, sys) 
        
if __name__ == '__main__':
    file_path = "Network_Data\phisingData.csv"
    database = "NetworkSecuroity"
    collection = "NetworkData"
    data_extract_obj = NetworkDataExtract()
    records = data_extract_obj.csv_to_json_conveter( file_path = file_path)
    no_of_records = data_extract_obj.insert_data_monfoDB(records, database, collection)
    # print(no_of_records)