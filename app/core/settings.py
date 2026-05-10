from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Buscador Semântico de Repositórios"
    APP_VERSION: str = "0.2.0"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://synapse:synapse@localhost:5432/synapse_search"
    VECTOR_DIMENSION: int = 384

    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


settings = Settings()