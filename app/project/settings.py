from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    run_mode: Literal["dev", "stage", "prod"] = "dev"

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env.dev')


settings = AppSettings()
