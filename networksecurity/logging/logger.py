## We create a logger.py file to record everything that happens inside our project. like Inof, warning , error

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"   # it create the file name , file is NOT created yet.
logs_folder = os.path.join(os.getcwd(), "logs")  # Creating Logs Folder Path , log is the folder name ,  still file is NOT created yet.
os.makedirs(logs_folder, exist_ok=True)   # here the folder is created

LOG_FILE_PATH = os.path.join(logs_folder, LOG_FILE)  # creating the log file, like:- C:/Users/Ankesh/project/logs/02_27_2026_16_20_15.log


# Configure logging system
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)



# it create the logging file 
'''
if __name__ =="__main__":
    logging.info("Logging has started")
'''