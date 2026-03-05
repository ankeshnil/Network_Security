# the output of the data ingestion is  data injestion artifact

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str