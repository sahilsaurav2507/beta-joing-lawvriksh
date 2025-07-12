import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "lawviksh_db"
    db_user: str = "root"
    db_password: str = "Sahil@123"
    
    # Security Configuration
    secret_key: str = "dsjdnfvndvndofhgofdhguhduigfhdofoidfjjpj8475nfjo"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Admin Credentials
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 