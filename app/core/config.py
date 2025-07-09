import os


class Settings:
    PAGINATION_LIMIT: int = 25

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ems")

    SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


"""
define env based settings, if required

class ProdSettings(Settings):
    key = "prod value"
"""
# choose settings based on current env (if multiple env based settings used)
settings = Settings()