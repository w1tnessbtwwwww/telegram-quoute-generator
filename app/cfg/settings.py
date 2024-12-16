from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str


settings = Settings()