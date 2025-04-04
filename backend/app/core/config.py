from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./social_auto.db"
    SECRET_KEY: str = "your_secret_here"

    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_BEARER_TOKEN: str

    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str
    TWITTER_REDIRECT_URI: str

    class Config:
        env_file = ".env"

settings = Settings()

# from pydantic_settings import BaseSettings
# from pydantic import Field


# class Settings(BaseSettings):
#     # Core app settings
#     DATABASE_URL: str = "sqlite:///./social_auto.db"
#     SECRET_KEY: str = "your_secret_here"

#     # Twitter API credentials
#     TWITTER_API_KEY: str = Field(..., alias="TWITTER_API_KEY")
#     TWITTER_API_SECRET: str = Field(..., alias="TWITTER_API_SECRET")
#     TWITTER_ACCESS_TOKEN: str = Field(default="", alias="TWITTER_ACCESS_TOKEN")
#     TWITTER_ACCESS_SECRET: str = Field(default="", alias="TWITTER_ACCESS_SECRET")

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#         extra = "ignore"  # Prevent crashing on unrelated env keys


# settings = Settings()

