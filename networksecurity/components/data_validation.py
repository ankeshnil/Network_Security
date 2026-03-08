import os  # it can do Create folders, Join file paths properly, check if file exist 
import sys
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils import write_yaml_file
from networksecurity.entity.comfig_entity import DataValicationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.constant.traning_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config: DataValicationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkException(e, sys)
        
    def read_data(self, file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkException(e,sys)
        
    def validate_number_column(self, dataFrame : pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"number of columns requiremnt:{number_of_columns}")
            if len(dataFrame.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkException(e,sys)
        
    def validate__column_datatype(self, DataFrame: pd.DataFrame) -> bool:
            try:
                schema_columns = self._schema_config["columns"]

                for column in DataFrame.columns:
                    if column not in schema_columns:
                        logging.error(f"{column} not found in schema")
                        return False

                    expected_schema = schema_columns[column]
                    actual_schema = str(DataFrame[column].dtype)

                    if expected_schema != actual_schema:
                        logging.error(f"Datatype mismatch in {column}")
                        return False

                return True

            except Exception as e:
                raise NetworkException(e, sys)
        
 # base_df= It represents the original data distribution.   current_df = is the new dataset you want to check.  
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        try:
            status = True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                
                is_same_dist = ks_2samp(d1,d2)  # it chech the drift
                
                if threshold <= is_same_dist.pvalue:
                    if_found = False
                else:
                    if_found = True
                    status = False  # becasue true hoa mane dictribution change hoa che 
                    report.update({column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status": if_found
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            # create Disctnary
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path= drift_report_file_path, content= report)
            return status
        except Exception as e:
            raise NetworkException(e,sys)
        
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_DataFrame = self.read_data(train_file_path)
            test_DataFrame = self.read_data(test_file_path)
            
            # check number of columns
            status = self.validate_number_column(train_DataFrame)
            if status == False:
                error_message = f"Train DataFrame does not match all the columns"

            status = self.validate_number_column(test_DataFrame)
            if status == False:
                error_message = f"Test DataFrame does not match all the columns"

            # check datatype
            status = self.validate__column_datatype(train_DataFrame)
            if status == False:
                error_message = f"Train DataFrame does not match all the columns datatype"

            status = self.validate__column_datatype(test_DataFrame)
            if status == False:
                error_message = f"Test DataFrame does not match all the columns datatype"
                
            # Check the data drift
            status= self.detect_dataset_drift(base_df= train_DataFrame, current_df= test_DataFrame)
            
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path) # create the path where we store validation train and test data
            os.makedirs(dir_path, exist_ok=True)  # create the folder  
            train_DataFrame.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header =True
            )
            test_DataFrame.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header =True
            )
            
            
            # return componenets 
            Data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path,
                )

            return Data_validation_artifact
        except Exception as e:
            raise NetworkException(e,sys)