from dataclasses import dataclass
from environs import Env

@dataclass
class Postgres:
    user: str
    password: str
    db: str
    url: str

@dataclass
class Redis:
    host: str
    port: int
    db: int

@dataclass
class Config:
    postgres: Postgres
    redis: Redis

def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(
        postgres=Postgres(
            user=env("POSTGRES_USER"),
            password=env("POSTGRES_PASSWORD"),
            db=env("POSTGRES_DB"),
            url=env("POSTGRES_URL"),
                          ),
        redis=Redis(host=env("REDIS_HOST"),
                    port=env.int("REDIS_PORT"),
                    db=env.int("REDIS_DB"),
                    ),
    )
config = load_config()
