# Settings via pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="HN_")

    base_url: str = "https://news.ycombinator.com"
    max_pages: int = 3
    rate_limit: float = 1.5
    output_dir: str = "./data"
    log_level: str = "INFO"


settings = Settings()