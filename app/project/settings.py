from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class AppSettings(BaseSettings):
    run_mode: Literal["dev", "stage", "prod"] = "dev"
    rabbit_user: str = "guest"
    rabbit_password: str = "guest"
    rabbit_host: str = "events-rabbit"
    rabbit_port: int = 5672
    rabbit_events_queue_name: str = "events_queue"
    users_service_grpc: str = "users-service:9090"

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env.dev')


settings = AppSettings()
