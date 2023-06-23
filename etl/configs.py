from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):

    host: str = Field(..., env="DB_HOST")
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    dbname: str = Field(..., env="DB_NAME")
    port: int = Field(..., env="DB_PORT")
    options: str = Field(..., env="DB_options")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def postgresql_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class ElasticConfig(BaseSettings):
    host: str = Field("localhost", env="ELASTIC_HOST")
    port: int = Field(9200, env="ELASTIC_PORT")

    @property
    def elastic_dsn(self):
        return f"http://{self.host}:{self.port}/"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


class ETLConfig(BaseSettings):
    start_sleep_time = 0.1
    factor = 2
    border_sleep_time = 10
    storage_file_path = 'states.json'
    batch_size = 1000


postgres_settings = PostgresConfig()
elastic_setings = ElasticConfig()
etl_settings = ETLConfig()
