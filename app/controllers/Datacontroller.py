from fastapi import UploadFile
from .BaseController import BaseController
from .project_controller import ProjectController
import re
import os
from app.models.enums.response_signal import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()

            
    def validate_upload_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        if file.size > self.app_settings.MAX_FILE_SIZE:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True , ResponseSignal.FILE_VALIDATION_SUCCESS.value


    def  generate_unique_file_path(self,orig_file_name:str,project_id:str ):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_file_name = self.get_clean_filename(
            orig_file_name=orig_file_name
            )

        new_file_name = os.path.join(
            project_path,   
            random_key+"_"+clean_file_name
        )

        while os.path.exists(new_file_name):
            random_key = self.generate_random_string()
            new_file_name = os.path.join(
                project_path,
                random_key+"_"+clean_file_name
            )
        
        file_id = random_key+"_"+clean_file_name
        return new_file_name, file_id



    
    def get_clean_filename(self,orig_file_name:str):    
        

        clean_file_name = re.sub(r'[^\w.]','',orig_file_name.strip())
        clean_file_name = clean_file_name.replace(" ","_")
        return clean_file_name


        