from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str = "postgres"
    database_password: str = "postgres"
    DATABASE_HOSTNAME:str="localhost"
    DATABASE_PORT:int=5432
    DATABASE_NAME:str="postgres"
    SECRET_KEY:str = "FDKJGSD983479CVNGSKLJF3498759SDJKLF3DSFLKJ239847RDAJ3"
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30

    class Config:
        env_file = ".env"

settings = Settings()
