import sys
import logging
from networksecurity.logging.logger  import logging

def error_message_details(error, error_details:sys):
    _,_,exc_tb = error_details.exc_info()  # there this exc_info give 3 info. but we need only 3rd info(exc_tab) , it say where the error hapend
    file_name = exc_tb.tb_frame.f_code.co_filename # it give the occre error file name
    error_message = "Error occred in python script name [{0}] line number [{1}] error message [{0}]".format(file_name, exc_tb.tb_lineno, str(error))
    return error_message


class NetworkException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)   # Call the parent class constructor and pass the error message to it.
        self.error_message = error_message_details(error_message, error_details= error_detail)
        
    def __str__(self):
        return self.error_message  # here the error message get print
    
    
''' 
if __name__ =="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Devide by zero error   in expection folder ")
        raise NetworkException(e,sys)
'''