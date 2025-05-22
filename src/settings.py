from pydantic_settings import SettingsConfigDict, BaseSettings



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEV_MODE: bool = False

    # Model
    MODEL_PATH: str
    NMS_THRESHOLD: float = 0.5

    # image processing
    WIN_SIZE: int
    STRIDE: int


settings = Settings()