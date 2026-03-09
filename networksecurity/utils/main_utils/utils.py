import yaml
from networksecurity.exception.excetion import NetworkException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import sys
import os
import pickle


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkException(e, sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise NetworkException(e, sys)
    
def save_numoy_array_data (file_path: str, array: np.array):  # save numpy array data to file
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None: # We use KNN imputer so i have to same it as .pkl file
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exicted the save obj method")
    except Exception as e:
        raise NetworkException(e, sys) from e