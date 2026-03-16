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
     
     
class DataTransformationConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, traning_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transfrom_train_file_path: str = os.path.join(self.data_transformation_dir, traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                traning_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transfrom_test_file_path: str = os.path.join(self.data_transformation_dir, traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                traning_pipeline.TEST_FILE_NAME.replace("csv", "npy"),)
        self.transfrom_obj_file_path: str= os.path.join(self.data_transformation_dir, traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                        traning_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
     

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir : str = os.path.join(training_pipeline_config.artifact_dir,
                                        traning_pipeline.MODEL_TRAINER_DIR_NAME)
        self.train_model_file_path : str = os.path.join(self.model_trainer_dir, traning_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                  traning_pipeline.MODEL_FILE_NAME)
     
        self.expected_accurecy : float = traning_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfiting_underfiting_thresold = traning_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        
'''
Artifacts/
│
└── 03_09_2026_09_30_15/                 ← timestamp created by TrainingPipelineConfig
    │
    ├── data_ingestion/
    │   │
    │   ├── feature_store/
    │   │       └── phisingData.csv      ← feature_store_file_path
    │   │
    │   └── ingested/
    │           ├── train.csv            ← train_file_path
    │           └── test.csv             ← test_file_path
    │
    ├── data_validation/
    │   │
    │   ├── validated/
    │   │       ├── train.csv            ← valid_train_file_path
    │   │       └── test.csv             ← valid_test_file_path
    │   │
    │   ├── invalid/
    │   │       ├── train.csv            ← invalid_train_file_path
    │   │       └── test.csv             ← invalid_test_file_path
    │   │
    │   └── drift_report/
    │           └── report.yaml          ← drift_report_file_path
    │
    └── data_transformation/
        │
        ├── transformed/
        │       ├── train.npy            ← transformed_train_file_path
        │       └── test.npy             ← transformed_test_file_path
        │
        └── transformed_object/
                └── preprocessing.pkl    ← transformed_object_file_path
'''