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

    client_id: str
    client_secret: str

    api_link: str

    rabbitmq_default_user: str
    rabbitmq_default_pass: str

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

    def get_mongo_uri(self):
        user = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        name = self.postgres_db
        return f'mongodb://{user}:{password}@{host}:27017'

    def get_rabbitmq_uri(self):
        user = self.rabbitmq_default_user
        password = self.rabbitmq_default_pass
        host = self.postgres_host
        return f'amqp://{user}:{password}@{host}'


settings = Settings()
