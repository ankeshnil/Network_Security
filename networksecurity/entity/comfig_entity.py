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


class DataValicationConfig:
    def __init__(self, Training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            Training_pipeline_config.artifact_dir,  traning_pipeline.DATA_VALIDATION_DIR_NAME)
        
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,  traning_pipeline.DATA_VALIDATION_INVALID_DIR)
        
        self.invalid_data_dir :str = os.path.join(
            self.data_validation_dir, traning_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        
        self.valid_train_file_path : str= os.path.join(
            self.valid_data_dir, traning_pipeline.TRAIN_FILE_NAME
        )
        
        self.valid_test_file_path :str = os.path.join(
            self.valid_data_dir, traning_pipeline.TEST_FILE_NAME
        )
        
        self.invalid_train_file_path : str= os.path.join(
            self.invalid_data_dir, traning_pipeline.TRAIN_FILE_NAME
        )
        
        self.invalid_test_file_path :str = os.path.join(
            self.invalid_data_dir, traning_pipeline.TEST_FILE_NAME
        )
        
        self.drift_report_file_path :str = os.path.join(
            self.data_validation_dir,
            traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            traning_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME 
        )
        
'''
Artifacts/
│
└── 03_04_2026_18_10_22/                ← timestamp created by TrainingPipelineConfig
    │
    ├── data_ingestion/
    │   │
    │   ├── feature_store/
    │   │       └── phisingData.csv     ← feature_store_file_path
    │   │
    │   └── ingested/
    │           ├── train.csv           ← train_file_path
    │           └── test.csv            ← test_file_path
    │
    └── data_validation/
        │
        ├── validated/
        │       ├── train.csv           ← valid_train_file_path
        │       └── test.csv            ← valid_test_file_path
        │
        ├── invalid/
        │       ├── train.csv           ← invalid_train_file_path
        │       └── test.csv            ← invalid_test_file_path
        │
        └── drift_report/
                └── report.yaml         ← drift_report_file_path
'''