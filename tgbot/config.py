import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    use_redis: bool
    use_db: bool
    orders_group: str
    couriers_group: str
    events_group: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            use_redis=cast_bool(tg_bot.get("use_redis")),
            use_db=cast_bool(tg_bot.get("use_db")),
            orders_group=tg_bot["orders_group"],
            couriers_group=tg_bot["couriers_group"],
            events_group=tg_bot["events_group"],
        ),
        db=DbConfig(**config["db"])
    )
