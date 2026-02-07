from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str
    APP_ENV:str
    DEBUG: bool = False 
    # REDIS_URL : str
    # REDIS_HOST:str
    # REDIS_PORT:int
    ACCESS_TOKEN_EXPIRE_SECONDS:int
    OTP_TOKEN_EXPIRE_SECONDS:int
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str
    SUPERADMIN_NAME:str
    SUPERADMIN_EMAIL:str
    SUPERADMIN_PASSWORD:str
    SUPERADMIN_PHONE:str
    MAIL_SERVER:str
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_PORT:int
    MAIL_FROM:str
    

    class Config:
        env_file = ".env"
        extra="forbid"

settings = Settings()