from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
from networksecurity.entity.comfig_entity import Dataingestionconfig
from networksecurity.entity.comfig_entity import TrainingPipelineConfig

import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = Dataingestionconfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        logging.info("Initiate the data ingestion")

        dataingestionartifact = data_ingestion.initiate_data_ingestion()

        print(dataingestionartifact)

    except Exception as e:
        raise NetworkException(e, sys)