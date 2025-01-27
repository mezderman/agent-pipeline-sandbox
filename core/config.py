from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # "gpt-4o-2024-08-06"
    OPENAI_MODEL: str = "gpt-3.5-turbo-0125" 
    # Add other global settings here

settings = Settings() 