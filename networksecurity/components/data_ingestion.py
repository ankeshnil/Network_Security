import os  # it can do Create folders, Join file paths properly, check if file exist 
import sys
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from networksecurity.entity.comfig_entity import Dataingestionconfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL") 

class DataIngestion:
    def __init__(self, data_ingestion_config : Dataingestionconfig ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e :
            raise NetworkException(e, sys)
        logging.info("crete data_ingestion_config object ")
    
    def export_collection_as_dataframe(self): # read dataframe form mongodb
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.Mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.Mongo_client[database_name][collection_name]  # [networksecurity][phishingData]
            
            '''
            collection stor data in document format in key value pair  line { "URL_Length": -1, "having_IP_Address": 1, "Result": -1 }
            when we run .find we get a cursor object.
            Because find() returns a cursor, but Pandas needs a list of dictionaries.
            '''
            df = pd.DataFrame(list(collection.find())) 
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], inplace=True)
            df.replace({"na": np.nan},inplace=True)
            return df
             
            logging.info("data extract form MongoDb Datavase")
            
        except Exception as e :
            raise NetworkException(e, sys)
        
        
    def export_data_into_featurestore(self, Dataframe : pd.DataFrame):
        try:
            feature_file_path = self.data_ingestion_config.feature_store_file_path
            #creating the folder 
            dir_path = os.path.dirname(feature_file_path) # extract the folder path 
            os.makedirs(dir_path, exist_ok=True)
            Dataframe.to_csv(feature_file_path, index=False, header=True)
            return Dataframe
            logging.info("create the arifact folder ")
        
        except Exception as e :
            raise NetworkException(e, sys)
        
        
    def split_Data_train_test(self, dataframe : pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe,  test_size= self.data_ingestion_config.train_test_split)
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=True, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=True, header=True)
            logging.info("Done train test split")
        except Exception as e :
            raise NetworkException(e, sys)
            
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_featurestore(dataframe)
            self.split_Data_train_test(dataframe)
            
            dataingestionartifact = DataIngestionArtifact(
                        trained_file_path= self.data_ingestion_config.train_file_path,
                        test_file_path = self.data_ingestion_config.test_file_path)
            
            return dataingestionartifact
            logging.info("Data Ingestion Complete")
            
        except Exception as e :
            raise NetworkException(e, sys)