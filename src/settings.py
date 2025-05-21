from pydantic_settings import SettingsConfigDict, BaseSettings



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000


settings = Settings()