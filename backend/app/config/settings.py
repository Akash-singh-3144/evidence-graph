from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "EvidenceGraph API"
    VERSION: str = "1.0.0"

    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"
    EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSION: int = 768

    # App database
    APP_DB_HOST: str
    APP_DB_PORT: int
    APP_DB_USER: str
    APP_DB_PASSWORD: str
    APP_DB_NAME: str

    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.APP_DB_USER}:{self.APP_DB_PASSWORD}@{self.APP_DB_HOST}:{self.APP_DB_PORT}/{self.APP_DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
