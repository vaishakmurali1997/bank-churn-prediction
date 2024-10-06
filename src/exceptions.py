import sys

def error_message_detail(error, error_detail:sys):
    _,_,err_tb = error_detail.exc_info()
    filename = err_tb.tb_frame.f_code.co_filename
    message = "Error:  [{0}] line number [{1}] message: [{2}]".format(
        filename, err_tb.tb_lineno, str(error))
    return message
    
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
    
    def __str__(self) -> str:
        return self.error_message