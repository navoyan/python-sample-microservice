from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017/"
    database_name: str = "document-fastapi-sample"
    collection_name: str = "documents"


settings = Settings()
