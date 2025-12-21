from enum import Enum 


class response_signal(Enum):
    FILE_VALIDATION_SUCCESS = "file_validation_success"
    FILE_TYPE_NOT_ALLOWED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"