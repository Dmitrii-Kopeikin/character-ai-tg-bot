from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Bot(BaseModel):
    token: str
    webhook_path: str


class Server(BaseModel):
    host: str
    port: int


class Postgres(BaseModel):
    user: str
    password: str
    host: str
    inner_host: str
    port: int
    db: str

    inner_url: str | None = None
    url: str | None = None

    sync_inner_url: str | None = None
    sync_url: str | None = None

    @validator("inner_url", always=True)
    def _create_inner_url(cls, v, values) -> str:
        return (
            f"postgresql+asyncpg://{values['user']}:{values['password']}@"
            f"{values['inner_host']}:{values['port']}/{values['db']}"
        )

    @validator("url", always=True)
    def _create_url(cls, v, values) -> str:
        return (
            f"postgresql+asyncpg://{values['user']}:{values['password']}@"
            f"{values['host']}:{values['port']}/{values['db']}"
        )

    @validator("sync_inner_url", always=True)
    def _create_sync_inner_url(cls, v, values) -> str:
        return (
            f"postgresql+psycopg2://{values['user']}:{values['password']}@"
            f"{values['inner_host']}:{values['port']}/{values['db']}"
        )

    @validator("sync_url", always=True)
    def _create_sync_url(cls, v, values) -> str:
        return (
            f"postgresql+psycopg2://{values['user']}:{values['password']}@"
            f"{values['host']}:{values['port']}/{values['db']}"
        )


class Redis(BaseModel):
    host: str
    port: int
    password: str
    db: int

    url: str | None = None

    @validator("url", always=True)
    def _create_url(cls, v, values) -> str:
        return (
            f"redis://:{values['password']}@"
            f"{values['host']}:{values['port']}/{values['db']}"
        )


class Amplitude(BaseModel):
    api_key: str


class OpenAI(BaseModel):
    model: str
    max_tokens: int
    context_requests_count: int
    gateway: str
    api_key: str
    request_attempts: int


class Debug(BaseModel):
    enabled: bool


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    server: Server
    postgres: Postgres
    redis: Redis
    bot: Bot
    amplitude: Amplitude
    open_ai: OpenAI
    debug: Debug


config = Config()
