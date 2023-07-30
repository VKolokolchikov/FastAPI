"""Settings module"""

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """App settings"""

    debug: bool = True
    db_logs: bool = False
    host: str = 'localhost'
    port: int = 8000
    date_format: str = '%d.%m.%Y'
    datetime_format: str = '%d.%m.%Y %H:%M:%S'
    service_name: str = ''
    db_name: str = ''
    db_host: str = 'localhost'
    db_host_ro: str | None = None
    db_port: int = 5435
    db_port_ro: int | None = None
    db_user: str = ''
    db_password: str = ''

    # Validation constants
    tg_secret_key: str = ''
    tg_constant_string: str = 'WebAppData'
    tg_separate_hash: str = '&hash='
    tg_separate_symbol: str = '&'
    tg_join_symbol: str = '\n'

    @property
    def db_url(self) -> PostgresDsn:
        """Make db url from params"""
        return PostgresDsn(
            url=(
                f'postgresql+asyncpg://{self.db_user}:{self.db_password}'
                f'@{self.db_host}:{self.db_port}/{self.db_name}'
            ),
            scheme='postgresql+asyncpg'
        )

    @property
    def db_url_ro(self) -> PostgresDsn | None:
        """Make db url from params"""
        if self.db_host_ro is None or self.db_port_ro is None:
            return None

        return PostgresDsn(
            url=(
                f'postgresql+asyncpg://{self.db_user}:{self.db_password}'
                f'@{self.db_host_ro}:{self.db_port_ro}/{self.db_name}'
            ),
            scheme='postgresql+asyncpg'
        )

    class Config:  # pylint: disable=too-few-public-methods
        """Prefix config"""
        env_prefix = 'api_'
        env_file = ".env"


settings = Settings()
