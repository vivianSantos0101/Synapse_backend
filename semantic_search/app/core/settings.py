from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Buscador Semântico de Repositórios"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "readmes"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    GITHUB_TOKEN: str | None = None
    GITHUB_ORG: str | None = None

settings = Settings()