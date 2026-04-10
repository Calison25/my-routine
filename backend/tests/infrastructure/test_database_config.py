import os

from app.infrastructure.database.config import DatabaseSettings


class TestDatabaseConfig:
    def test_database_settings_reads_env(self, monkeypatch: object) -> None:
        custom_url = "postgresql+asyncpg://custom:custom@db:5432/test_db"
        monkeypatch.setenv("DATABASE_URL", custom_url)  # type: ignore[attr-defined]

        settings = DatabaseSettings()

        assert settings.DATABASE_URL == custom_url

    def test_database_settings_has_default(self) -> None:
        env_backup = os.environ.pop("DATABASE_URL", None)
        try:
            settings = DatabaseSettings()
            assert "postgresql+asyncpg://" in settings.DATABASE_URL
            assert "my_routine" in settings.DATABASE_URL
        finally:
            if env_backup is not None:
                os.environ["DATABASE_URL"] = env_backup
