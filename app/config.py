from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    mysql_database: str
    mysql_user: str
    mysql_password: str


settings = Settings()
