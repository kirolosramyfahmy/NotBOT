from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/sentinel_core"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
