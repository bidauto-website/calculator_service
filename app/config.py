from enum import Enum

from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Permissions(str, Enum):
    EXCHANGE_RATE_WRITE = "calculator.exchange-rate:write"


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "testpass"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Application
    APP_NAME: str = "calculator-service"
    DEBUG: bool = True
    ROOT_PATH: str = ''
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # RPC
    RPC_API_URL: str = "localhost:50051"

    @property
    def enable_docs(self) -> bool:
        return self.ENVIRONMENT in [Environment.DEVELOPMENT]

settings = Settings()
