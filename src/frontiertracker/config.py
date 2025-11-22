
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    database_url: str = "sqlite:///./dev.db"
    debug: bool = False

settings = Settings()

if __name__ == "__main__":
    print(f"Database URL: {settings.database_url}")
    print(f"Debug Mode: {settings.debug}")