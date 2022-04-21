from aiogram import Bot, Dispatcher, types
from data.config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.sqlite import Database
from loguru import logger


logger.add("data/info.log", format="{time} {level} {message}", level="DEBUG")
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
