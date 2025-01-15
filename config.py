from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    email_address: str
    email_password: str
    email_server: str

    jwt_secret: str

    api_link: str
    files_dir: str = 'assets/images'
    upload_dir: str = 'static'
    date_format: str = '%Y-%m-%d'
    date_time_format: str = '%Y-%m-%d %H:%M'

    model_config = SettingsConfigDict(env_file='.env')

    def get_async_uri(self):
        user = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        name = self.postgres_db
        result = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'
        return result

    def get_uri(self):
        user = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        name = self.postgres_db
        return f'postgresql://{user}:{password}@{host}:{port}/{name}'


settings = Settings()
