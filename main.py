from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.entity.comfig_entity import Dataingestionconfig, DataValicationConfig, DataTransformationConfig
from networksecurity.entity.comfig_entity import TrainingPipelineConfig
import yaml
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = Dataingestionconfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiate the data ingestion")

        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        
        logging.info("Data ingestion completed")
        print(dataingestionartifact)
        
        data_validation_config= DataValicationConfig(trainingpipelineconfig)
        data_validation =DataValidation(data_validation_config,dataingestionartifact )
        logging.info("Initiate Data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation Completed")
        print(data_validation_artifact)
        
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("Initiate Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation() 
        logging.info("Data transformation Completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkException(e, sys)