import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
        self.password_salt = os.getenv("PASSWORD_SALT", "securevault-salt")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///securevault.db")
        self.jwt_expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
        self.environment = os.getenv("APP_ENV", "production")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cors_origins = os.getenv("CORS_ORIGINS", "*")
        self.max_content_length = int(os.getenv("MAX_CONTENT_LENGTH", "1048576"))
        self.api_version = os.getenv("API_VERSION", "v1")

    def flask_config(self) -> dict:
        return {
            "SECRET_KEY": self.secret_key,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_EXPIRATION_HOURS": self.jwt_expiration_hours,
            "MAX_CONTENT_LENGTH": self.max_content_length,
        }
