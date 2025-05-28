from pydantic_settings import SettingsConfigDict, BaseSettings



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEV_MODE: bool = False

    # Model
    MODEL_PATH: str

    # Image processing
    WIN_SIZE: int
    STRIDE: int
    BATCH_SIZE: int

    # Postprocessing 
    CONFS_THRESHOLD: float
    NMS_THRESHOLD_BOXES: float

    # Coordinates consts
    METERS_PER_PIXEL: float
    R_EARTH: int




settings = Settings()