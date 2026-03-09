# the output of the data ingestion confonent is  data injestion artifact
# and this is also input fot data validation componenet
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
    
# here we write the output of data validation part
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path :str
    valid_test_file_path :str
    invalid_train_file_path :str
    invalid_test_file_path :str
    drift_report_file_path :str
    
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path : str
    transformed_train_file_path : str
    transformed_test_file_path : str
    