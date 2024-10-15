from aiogram.types import Message, CallbackQuery, KeyboardButton, InlineKeyboardButton, KeyboardButtonRequestUser
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardMarkup
from db.db import Database

db = Database('db.db')

admins = [5140064907, 725473993, 495291346]

def get_user_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="💥 Скидки и акции")
        )
    builder.row(
        KeyboardButton(text="✍️ О нас")
        )
    return builder.as_markup(resize_keyboard=True)

def greet_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🤩 Поехали")
        )
    return builder.as_markup(resize_keyboard=True)

def cancel_btn():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Или нажмите на 'ОТМЕНА' для отмены"
    )

def admin_kb(id):
    if id in admins:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
                [InlineKeyboardButton(text="📧 Рассылка всем", callback_data="admin_broadcast")],
                [InlineKeyboardButton(text="🙅‍♀️ Рассылка нелояльным", callback_data="admin_broadcast_not_active")],
                [InlineKeyboardButton(text="🗒️ Список админов", callback_data="admin_list")],
                [InlineKeyboardButton(text="➕ Назначить админа", callback_data="add_admin")],
                [InlineKeyboardButton(text="➖ Удалить админа", callback_data="del_admin")]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
                [InlineKeyboardButton(text="📧 Рассылка всем", callback_data="admin_broadcast")],
                [InlineKeyboardButton(text="🙅‍♀️ Рассылка нелояльным", callback_data="admin_broadcast_not_active")]
            ]
        )
    return keyboard

def done_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data='done')],
            [InlineKeyboardButton(text="😢 Нужна помощь", callback_data='idk')]
        ]
    )
    return keyboard

def how_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Регистрация", url='https://app.loona.ai/3866/create?source=Telegram&tag=link')],
            [InlineKeyboardButton(text="✅ Получилось!", callback_data='done')]
        ]
    )
    return keyboard

def start_kb(id):
    try:
        if not db.user_active(id):
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                [InlineKeyboardButton(text="👋 Кто мы", callback_data="about")],
                [InlineKeyboardButton(text="🔍 Как нас найти", callback_data="where")],
                [InlineKeyboardButton(text="📺 Мы в социальных сетях", callback_data="sm")],
                [InlineKeyboardButton(text="🎤 Что о нас говорят", callback_data="reviews")],
                [InlineKeyboardButton(text="🍽️ Наше меню", url="https://hplife.ru/menu")],
                [InlineKeyboardButton(text="🎲 Наши настольные игры", callback_data="games")],
                [InlineKeyboardButton(text="💸 Получить 500 ₽", callback_data="gift")]
                ]
            )
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="👋 Кто мы", callback_data="about")],
                    [InlineKeyboardButton(text="🔍 Как нас найти", callback_data="where")],
                    [InlineKeyboardButton(text="📺 Мы в социальных сетях", callback_data="sm")],
                    [InlineKeyboardButton(text="🎤 Что о нас говорят", callback_data="reviews")],
                    [InlineKeyboardButton(text="🍽️ Наше меню", url="https://hplife.ru/menu")],
                    [InlineKeyboardButton(text="🎲 Наши настольные игры", callback_data="games")]
                ]
            )
    except:
        keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                [InlineKeyboardButton(text="👋 Кто мы", callback_data="about")],
                [InlineKeyboardButton(text="🔍 Как нас найти", callback_data="where")],
                [InlineKeyboardButton(text="📺 Мы в социальных сетях", callback_data="sm")],
                [InlineKeyboardButton(text="🎤 Что о нас говорят", callback_data="reviews")],
                [InlineKeyboardButton(text="🍽️ Наше меню", url="https://hplife.ru/menu")],
                [InlineKeyboardButton(text="🎲 Наши настольные игры", callback_data="games")],
                [InlineKeyboardButton(text="💸 Получить 500 ₽", callback_data="gift")]
                ]
            )
    return keyboard

def about_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="👋 Кто мы", callback_data="about")],
        [InlineKeyboardButton(text="🔍 Как нас найти", callback_data="where")],
        [InlineKeyboardButton(text="📺 Мы в социальных сетях", callback_data="sm")],
        [InlineKeyboardButton(text="🎤 Что о нас говорят", callback_data="reviews")],
        [InlineKeyboardButton(text="🍽️ Наше меню", url="https://hplife.ru/menu")],
        [InlineKeyboardButton(text="🎲 Наши настольные игры", callback_data="games")]
        ]
    )
    return keyboard

def add_admin_kb():
    buttons = [
        [
            KeyboardButton(
                text="👤 Выбрать",
                request_user=KeyboardButtonRequestUser(
                    request_id=1,
                    user_is_bot=False
                )
            )
        ],
        [
            KeyboardButton(
                text="❌ Отмена"
            )
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите админа"
    )

    return keyboard