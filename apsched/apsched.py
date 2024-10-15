from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from db.db import Database
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from random import choice
from datetime import datetime, timedelta
import pytz
from aiogram import Bot
from config import config
from keyboards.kb import done_kb
from aiogram.filters.callback_data import CallbackData
from asyncio import sleep

router = Router()
bot = Bot(token=config.bot_token.get_secret_value())

db = Database('db.db')

async def sendall():
    users = db.get_users()
    for i in users:
        try:
            if db.user_tryed(i[0]):
                if not db.user_active(i[0]):
                    db.day_count(i[0])
                    if db.get_day(i[0]) in [2, 4, 8, 15, 22, 29, 61, 91, 121, 151]:
                        try:
                            await bot.send_message(chat_id=i[0], text='Получилось забрать 500 бонусных рублей?', reply_markup=done_kb())
                        except:
                            db.delete_id(i[0])
        except: pass