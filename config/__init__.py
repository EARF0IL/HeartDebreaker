from dataclasses import dataclass
from environs import Env

from .lexicon import *
from .enums import *

@dataclass
class TgBot:
    token: str
    
@dataclass
class LLM:
    token: str
    url: str
    token: str
    temperature: float


@dataclass
class Config:
    tg_bot: TgBot
    llm: LLM
    database: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('TG_BOT_TOKEN')),
        database=env('DATABASE_URL'),
        llm = LLM(
            url=env('LLM_URL'),
            token=env('LLM_TOKEN'),
            temperature=float(env('LLM_TEMPERATURE'))
        )
    )