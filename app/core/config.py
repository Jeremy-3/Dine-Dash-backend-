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
    # M-Pesa
    MPESA_CONSUMER_KEY:    str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_SHORTCODE:       str = "174379"
    MPESA_PASSKEY:         str = ""
    MPESA_CALLBACK_URL:    str = ""
    MPESA_ENV:             str = "sandbox"  # "sandbox" or "production"

    @property
    def MPESA_BASE_URL(self) -> str:
        if self.MPESA_ENV == "production":
            return "https://api.safaricom.co.ke"
        return "https://sandbox.safaricom.co.ke"
    

    class Config: 
        env_file = ".env"
        extra="forbid"

settings = Settings()