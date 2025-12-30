from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str 
    JWT_SECRET:str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRY: int
    REFRESH_TOKEN_EXPIRY: int
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings() 