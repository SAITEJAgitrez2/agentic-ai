from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    postgres_url: str

    class Config:
        env_file = "env/.env"

settings = Settings()
