from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_string: str = "postgresql://postgres:postgres@localhost/db"
    
settings = Settings()