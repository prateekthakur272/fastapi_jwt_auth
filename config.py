from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL:str = 'sqlite:///db.sqlite3'
    
def get_settings() -> Settings:
    return Settings()