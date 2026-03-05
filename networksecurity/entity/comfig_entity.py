# Its job is only to store and generate all paths and settings used in the pipeline.

from datetime import datetime
import os
from networksecurity.constant import traning_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):  # create the artifact folder path
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = traning_pipeline.PIPELINE_NAME
        self.artifact_name = traning_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp: str = timestamp
        
class Dataingestionconfig:
    def __init__(self, Training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(Training_pipeline_config.artifact_dir, traning_pipeline.DATA_INGESTION_DIR_NAME )
        
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir,
                    traning_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
                    traning_pipeline.FILE_NAME )
        
        self.train_file_path: str = os.path.join(self.data_ingestion_dir,
                    traning_pipeline.DATA_INGESTION_INGESTED_DIR, 
                    traning_pipeline.TRAIN_FILE_NAME )
        
        self.test_file_path: str = os.path.join(self.data_ingestion_dir,
                    traning_pipeline.DATA_INGESTION_INGESTED_DIR, 
                    traning_pipeline.TEST_FILE_NAME )
        
        self.train_test_split : float= traning_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = traning_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str =  traning_pipeline.DATA_INGESTION_DATABASE_NAME
        
        
        
'''
Artifacts
   └── 03_04_2026_18_10_22
        └── data_ingestion
             ├── feature_store
             │      └── phisingData.csv
             │
             └── ingested
                    ├── train.csv
                    └── test.csv
'''