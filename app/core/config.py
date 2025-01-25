import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError

load_dotenv()


class Settings(BaseSettings):
    HF_ACCESS_TOKEN: str = Field(..., env="HF_ACCESS_TOKEN")
    HF_API_ENDPOINT: str = Field(..., env="HF_API_ENDPOINT")
    AZURE_STORAGE_CONNECTION_STRING: str = Field(..., env="AZURE_STORAGE_CONNECTION_STRING")
    GENERATED_IMAGES_CONTAINER_NAME: str = Field(..., env="GENERATED_IMAGES_CONTAINER_NAME")

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(f"Error loading settings: {e}")
