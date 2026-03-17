import os  # it can do Create folders, Join file paths properly, check if file exist 
import sys
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.traning_pipeline import TARGET_COLUMN
from networksecurity.constant.traning_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.entity.comfig_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numoy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkException(e,sys)
      
    @staticmethod  
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkException(e,sys)
        
    def get_data_trnasformer_object(self) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the
        training_pipeline.py file and returns a Pipeline object with the
        KNNImputer object as the first step.      Args=cls: DataTransformation  Returns: A Pipeline object
        """
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkException(e,sys)
        
    def initiate_data_transformation(self)-> DataTransformationArtifact : # return type is DataTransformationArtifact
        logging.info("initiate data transformation method")
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df =  DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            # ✅ ADD THIS BLOCK (VERY IMPORTANT)
            if "Unnamed: 0" in train_df.columns:
                train_df = train_df.drop(columns=["Unnamed: 0"])

            if "Unnamed: 0" in test_df.columns:
                test_df = test_df.drop(columns=["Unnamed: 0"])
                
            # traning dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            # traning dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            preprocessor = self.get_data_trnasformer_object()
            preprocessor_object =  preprocessor.fit(input_feature_train_df)
            transfrom_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transfrom_input_test_feature =  preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transfrom_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transfrom_input_test_feature, np.array(target_feature_test_df)]
            
            # Save numpy array data
            save_numoy_array_data(self.data_transformation_config.transfrom_train_file_path, array= train_arr,)
            save_numoy_array_data(self.data_transformation_config.transfrom_test_file_path, array= test_arr,)
            save_object(
    file_path=self.data_transformation_config.transfrom_obj_file_path,
    obj=preprocessor_object
)
            save_object("final_model/preprocessor.pkl", preprocessor_object)
            # preparing artifact    output
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transfrom_obj_file_path,
                transformed_train_file_path= self.data_transformation_config.transfrom_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transfrom_test_file_path
            )
            
            return data_transformation_artifact
            
            
            
            
        except Exception as e:
            raise NetworkException(e,sys)