import asyncio
from aiogram import Bot, Dispatcher, F
import logging
from config import config
from handlers import user_commands
from db.db import Database
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apsched import apsched 
from datetime import datetime, timedelta
import pytz
from aiogram.types import Message, CallbackQuery, KeyboardButton, InlineKeyboardButton, ChatJoinRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

db = Database('db.db')

scheduler = AsyncIOScheduler(timezone = "Europe/Moscow")
scheduler.add_job(apsched.sendall, trigger='cron', hour='20')

async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    scheduler.start()

    dp.include_routers(user_commands.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



