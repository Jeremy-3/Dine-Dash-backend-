from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str

    APP_ENV: str = "production"
    DEBUG: bool = False 

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600
    OTP_TOKEN_EXPIRE_SECONDS: int = 300

    JWT_SECRET_KEY: str = "not-secret-key"
    JWT_ALGORITHM: str = "HS256"

    SUPERADMIN_NAME: Optional[str] = None
    SUPERADMIN_EMAIL: Optional[str] = None
    SUPERADMIN_PASSWORD: Optional[str] = None
    SUPERADMIN_PHONE: Optional[str] = None


    # M-Pesa
    MPESA_CONSUMER_KEY: str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_SHORTCODE: str = "174379"
    MPESA_PASSKEY: str = ""
    MPESA_CALLBACK_URL: str = ""
    MPESA_ENV: str = "sandbox"

    # Flutterwave
    FLW_PUBLIC_KEY: str = ""
    FLW_SECRET_KEY: str = ""
    FLW_ENCRYPTION_KEY: str = ""
    FLW_CALLBACK_URL: str = ""
    FLW_REDIRECT_URL: str = ""
    FLW_ENV: str = "test"

    @property
    def FLW_BASE_URL(self) -> str:
        return "https://api.flutterwave.com/v3"

    @property
    def MPESA_BASE_URL(self) -> str:
        if self.MPESA_ENV == "production":
            return "https://api.safaricom.co.ke"
        return "https://sandbox.safaricom.co.ke"

    class Config:
        env_file = ".env"
        extra = "ignore"   # 🔥 IMPORTANT change