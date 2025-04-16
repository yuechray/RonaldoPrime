from src.core.settings import get_app_settings

settings=get_app_settings()

print(settings.postgres_dsn)