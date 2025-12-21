from fastapi import UploadFile
from .BaseController import BaseController

class DataController(BaseController):
    def __init__(self):
        super().__init__()

            
    def validate_upload_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWE_TYPES:
            return False , response_signal.FILE_TYPE_NOT_ALLOWED.value
        if file.size > self.app_settings.MAX_FILE_SIZE:
            return False , response_signal.FILE_SIZE_EXCEEDED.value

        return True , response_signal.FILE_VALIDATION_SUCCESS.value


        