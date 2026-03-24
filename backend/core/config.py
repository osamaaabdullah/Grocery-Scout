import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    #App
    app_name: str = "Grocery Scout"
    environment: str = "development"
    debug: bool = False
    website_url: str
    
    #Database
    database_url: str
    replica_database_url: str = ""
    
    #Redis
    redis_url: str = ""
    cache_ttl_seconds: int = 3600
    
    #Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 30
    
    #Geocode
    geocode_api_key: str
    
    #SMTP
    smtp_host: str = ""
    smtp_port: str = ""
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_mail_from: str = ""
    smtp_mail_name: str = ""
    smtp_mail_server: str = ""
    verification_token_expire_minutes: int = 10
    
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '..', '.env'), case_sensitive=False)
    
@lru_cache
def get_settings():
    return Settings()