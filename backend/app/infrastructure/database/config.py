from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/my_routine"
    )

    model_config = {"env_file": ".env", "extra": "ignore"}


database_settings = DatabaseSettings()
