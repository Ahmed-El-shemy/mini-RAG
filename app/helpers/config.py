from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILDE_ALLOWED_TYPES: list



    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
    