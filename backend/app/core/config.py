from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./social_auto.db"
    SECRET_KEY: str = "your_secret_here"

    class Config:
        env_file = ".env"

settings = Settings()

