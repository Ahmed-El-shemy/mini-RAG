from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list = ["application/pdf", "text/plain"]
    MAX_FILE_SIZE: int = 10485760  # 10MB
    FILE_CHUNK_SIZE: int = 1048576  # 1MB

    MONGODB_URL: str
    MONGODB_DATABASE: str
    

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
    