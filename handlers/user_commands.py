from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, InlineKeyboardButton, ChatJoinRequest, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from db.db import Database
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from random import choice
from datetime import datetime, timedelta
import pytz
from aiogram import Bot
from config import config
from aiogram.filters.callback_data import CallbackData
from asyncio import sleep
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apsched import apsched 
import asyncio
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from keyboards.kb import admin_kb, cancel_btn, get_user_kb, greet_kb, done_kb, start_kb, about_kb, add_admin_kb, how_kb

router = Router()
bot = Bot(token=config.bot_token.get_secret_value())

'''
class DayCallbackFactory(CallbackData, prefix="fabday"):
    day: str
'''

admins = [5140064907, 725473993, 495291346]

class Form(StatesGroup):
    start_broadcast = State()
    start_broadcast_not_active = State()
    add_admin = State()
    

router.message.filter(F.chat.type == "private")

db = Database('db.db')

scheduler = AsyncIOScheduler(timezone = "Europe/Moscow")

@router.chat_join_request()
async def he(link: ChatJoinRequest):
    await bot.approve_chat_join_request(link.chat.id, link.from_user.id)
    try:
        db.add_user(link.from_user.id, link.from_user.first_name)
    except: pass
    if link.from_user.id in admins:
        db.set_admin(link.from_user.id)
    if datetime.now().hour in [0, 1, 2, 3, 4, 5]:
        hello = 'Доброй ночи, '
    elif datetime.now().hour in [6, 7, 8, 9, 10, 11]:
        hello = 'Доброе утро, '
    elif datetime.now().hour in [18, 19, 20, 21, 22, 23]:
        hello = 'Добрый вечер, '
    else:
        hello = 'Добрый день, '
    
    try:
        hello += link.from_user.first_name+'👋\n\nЯ бот HP LIFE!\nЖмите "поехали", чтобы узнать о нас больше и получить 500 бонусных рублей'
    except: pass
    try:
        await bot.send_message(link.from_user.id,
            text=hello, reply_markup=greet_kb())
    except: pass

@router.message(Text('🤩 Поехали'))
async def menu(message: Message):
    try:
        await message.answer(
            text='Поехали!', reply_markup=get_user_kb())
        await message.answer(
            text=f'Через меня можно смотреть акции и многое другое.\nДля бронирования столика пишите нам в <a href="https://t.me/hplifechat">чат</a>.\nНе забудьте указать дату и время бронироввания, а также количество гостей.\n\nВозможно вы хотите узнать о нас больше:', reply_markup=start_kb(message.from_user.id), disable_web_page_preview=True, parse_mode="HTML"
            )
    except: pass

@router.message(Command(commands=["start"]))
async def start(message: Message):
    try:
        db.add_user(message.from_user.id, message.from_user.first_name)
    except: pass
    if message.from_user.id in admins:
        db.set_admin(message.from_user.id)
    if datetime.now().hour in [0, 1, 2, 3, 4, 5]:
        hello = 'Доброй ночи, '
    elif datetime.now().hour in [6, 7, 8, 9, 10, 11]:
        hello = 'Доброе утро, '
    elif datetime.now().hour in [18, 19, 20, 21, 22, 23]:
        hello = 'Добрый вечер, '
    else:
        hello = 'Добрый день, '
    try:
        hello += message.from_user.first_name
    except: pass
    try:
        await message.answer(
            text=hello, reply_markup=get_user_kb())
        await message.answer(
            text=f'Я бот HP LIFE.\nЧерез меня можно смотреть акции и многое другое.\nДля бронирования столика пишите нам в <a href="https://t.me/hplifechat">чат</a>.\nНе забудьте указать дату и время бронироввания, а также количество гостей.\n\nВозможно вы хотите узнать о нас больше:', reply_markup=start_kb(message.from_user.id), disable_web_page_preview=True, parse_mode="HTML"
            )
    except: pass

#Promo
@router.message(Text('💥 Скидки и акции'))
async def menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🤝 Пригласить друга и получить бонусы", 
        callback_data="friend"
        )
    try:
        if not db.user_active(message.from_user.id):
            builder.button(
                text="💸 Получить 500 ₽", 
                callback_data="gift"
                )
    except: pass
    builder.adjust(1)
    try:
        await message.answer(
            'Специальные предложения только для вас 😉', reply_markup=builder.as_markup(resize_keyboard=True)
        )
    except: pass

@router.callback_query(Text('games'))
async def change_contact(callback: CallbackQuery):
    try:
        await callback.message.answer('''У нас вы можете бесплатно поиграть во множество настольных игр!

Нарды
Шашки
Да-Нетки
Alias
UNO
Монополия
Имаджинариум
Бункер
Шахматы
Манчкин
Эпичные схватки боевых магов: Крутагидон 
Мемология

С радостью поможем Вам разобраться в правилах! Ждём в гости!''')
    except: pass

#Friend
@router.callback_query(Text('friend'))
async def change_contact(callback: CallbackQuery):
    if db.user_active(callback.from_user.id):
        builder = InlineKeyboardBuilder()
        builder.button(
            text="❓ Инструкция", 
            callback_data="howfr"
            )
        try:
            await callback.message.answer("Вы можете получить по 300 ₽ за каждого друга:", 
                reply_markup=builder.as_markup(resize_keyboard=True))
        except: pass
    else:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="💸 Оформить карту и получить 500 ₽", 
            callback_data="gift"
            )
        builder.button(
            text="👌 Я оформил карту", 
            callback_data="done"
            )
        builder.adjust(1)
        try:
            await callback.message.answer("Чтобы получить по 300 ₽ за каждого друга у вас должна быть наша карта лояльности.\nОформите карту и получите приветственные 500 ₽, и возвращайтесь 😉", 
                reply_markup=builder.as_markup(resize_keyboard=True))
        except: pass

@router.callback_query(Text('howfr'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🤖 Android", 
        callback_data="androidfr"
        )
    builder.button(
        text="🍏 iOS", 
        callback_data="iosfr"
        )
    builder.adjust(1)
    try:
        await callback.message.answer('Какое у вас устройство?', reply_markup=builder.as_markup(resize_keyboard=True)
        )
    except: pass

@router.callback_query(Text('androidfr'))
async def gift(callback: CallbackQuery):
    try:
        await callback.message.answer_photo(FSInputFile('androidfr1.png'),
            caption='1. Открываем Wallet Union и выбираем карту, нажав на нее. Затем нажимаем на три точки в верхнем правом углу.')
        await callback.message.answer_photo(FSInputFile('androidfr2.png'),
            caption='2. Находим реферальную ссылку и нажимаем на неё.')
        await callback.message.answer_photo(FSInputFile('andiosfr3.png'),
            caption='4. Нажимаем «Поделиться с другом» или копируем ссылку и отправляем другу.')
        await callback.message.answer('Готово!\n\nЕсли у вас возникли проблемы с реферальной ссылкой, вы можете написать в наш <a href="https://t.me/hplifechat">чат</a> или <a href="https://t.me/HookahPlaceLife">администратору</a>.\nМы с радостью поможем вам разобраться!', disable_web_page_preview=True, parse_mode="HTML")
    except: pass

@router.callback_query(Text('iosfr'))
async def gift(callback: CallbackQuery):
    try:
        await callback.message.answer_photo(FSInputFile('iosfr1.png'),
            caption='1. Открываем Apple Wallet и нажимаем на три точки в верхнем правом углу и нажимаем «Данные карты».')
        await callback.message.answer_photo(FSInputFile('iosfr2.png'),
            caption='2. Находим реферальную ссылку и нажимаем на неё.')
        await callback.message.answer_photo(FSInputFile('andiosfr3.png'),
            caption='4. Нажимаем «Поделиться с другом» или копируем ссылку и отправляем другу.')
        await callback.message.answer('Готово!\n\nЕсли у вас возникли проблемы с реферальной ссылкой, вы можете написать в наш <a href="https://t.me/hplifechat">чат</a> или <a href="https://t.me/HookahPlaceLife">администратору</a>.\nМы с радостью поможем вам разобраться!', disable_web_page_preview=True, parse_mode="HTML")
    except: pass

#500 реблсов
@router.callback_query(Text('gift'))
async def gift(callback: CallbackQuery):
    try:
        if not db.user_active(callback.from_user.id):
            try:
                db.set_tryed(callback.from_user.id)
            except: pass
            builder = InlineKeyboardBuilder()
            builder.button(
                text="❓ Инструкция", 
                callback_data="how"
                )
            builder.button(
                text="✅ Готово!", 
                callback_data="done"
                )
            builder.adjust(1)
            try:
                await callback.message.answer(
                    '''Пара формальностей и все готово:

1. Пройдите быструю регистрацию по <a href="tg://openmessage?user_id=https://app.loona.ai/3866/create?source=Telegram&tag=link">ссылке</a>

*Используйте настоящее имя и фамилию, чтобы получить бонус.

2. Возвращайтесь в чат и жмите «Готово!», чтобы дополнительно получить 300 бонусных рублей на ваш счёт! ↓''', reply_markup=builder.as_markup(resize_keyboard=True), disable_web_page_preview=True, parse_mode="HTML"
                    )
                await asyncio.sleep(300)
                await callback.message.answer('Получилось забрать 500 бонусных рублей?', reply_markup=done_kb()
                )
            except: pass
        else:
            builder = InlineKeyboardBuilder()
            builder.button(
            text="🤝 Пригласить друга и получить бонусы", 
            callback_data="friend"
            )
            try:
                await callback.message.answer(
                    '''Вы уже воспользовались этой акцией 😢

Но вы можете получить еще по 300 ₽ за каждого друга:Выбери вкладку «Пригласить друга и получить бонусы»''', reply_markup=builder.as_markup(resize_keyboard=True)
                )
                db.set_active(callback.from_user.id)
            except: pass
    except: pass

#gift done
@router.callback_query(Text('done'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🤝 Пригласи друга и получи бонусы", 
        callback_data="friend"
        )
    try:
        await callback.message.answer(
            '''Ура, на вашей бонусной карте уже 500 приветственных рублей!

Желаем продуктивной недели! И не забывайте про отдых!

Мы ждем вас, приходите к нам в гости и заново откройте для себя мир дымных кальянов и ароматного чая!

Вы можете получить еще по 300 ₽ за каждого друга:Выбери вкладку «Пригласить друга и получить бонусы»''', reply_markup=builder.as_markup(resize_keyboard=True)
        )
        db.set_active(callback.from_user.id)
    except: pass


@router.callback_query(Text('idk'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="❓ Инструкция", 
        callback_data="how"
        )
    try:
        await callback.message.answer(
            f'Если у вас возникли проблемы с регистрацией в программе лояльности, вы можете воспользоваться инструкцией либо написать в наш <a href="https://t.me/hplifechat">чат</a> или <a href="https://t.me/HookahPlaceLife">администратору</a>.\nМы с радостью поможем вам разобраться!', reply_markup=builder.as_markup(resize_keyboard=True), disable_web_page_preview=True, parse_mode="HTML"
        )
    except: pass

@router.callback_query(Text('how'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🤖 Android", 
        callback_data="android"
        )
    builder.button(
        text="🍏 iOS", 
        callback_data="ios"
        )
    builder.adjust(1)
    try:
        await callback.message.answer('Какое у вас устройство?', reply_markup=builder.as_markup(resize_keyboard=True)
        )
    except: pass

@router.callback_query(Text('android'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔗 Та самая ссылка", 
        url="https://app.loona.ai/3866/create?source=Telegram&tag=link"
        )
    try:
        await callback.message.answer('1. Переходим по ссылке.',
            reply_markup=builder.as_markup(resize_keyboard=True))
        await callback.message.answer_photo(FSInputFile('andios2.png'),
            caption='2. Заполняем регистрационную форму, отмечаем обязательные поля, и нажимаем «Получить карту».')
        await callback.message.answer_photo(FSInputFile('android3.png'),
            caption='3. Открывается окно с предложением добавить карту или скачать приложение:\n\nЕсли у вас нет приложения Wallet Union нажимаем «Скачать приложение». Откроется окно Google Play с нужным приложением, его нужно установить и открыть.')
        await callback.message.answer_photo(FSInputFile('android4.png'),
            caption='4. Далее нажимаем кнопку «Добавить в Wallet Union», затем «Сохранить» и карта добавится. ')
        await callback.message.answer('Готово!\n\nКак зарегистрируетесь, возвращайтесь в чат и жмите «Готово!», чтобы дополнительно получить 300 бонусных рублей на ваш счёт! ↓',
            reply_markup=how_kb())
    except: pass

@router.callback_query(Text('ios'))
async def gift(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔗 Та самая ссылка", 
        url="https://app.loona.ai/3866/create?source=Telegram&tag=link"
        )
    try:
        await callback.message.answer('1. Переходим по ссылке.',
            reply_markup=builder.as_markup(resize_keyboard=True))
        await callback.message.answer_photo(FSInputFile('andios2.png'),
            caption='2. Заполняем регистрационную форму, отмечаем обязательные поля, и нажимаем «Получить карту».')
        await callback.message.answer_photo(FSInputFile('ios3.png'),
            caption='3. В открывшемся окне нажимаем на кнопку «Добавить в Apple Wallet».')
        await callback.message.answer_photo(FSInputFile('ios4.png'),
            caption='4. На всплывающем поп-апе нажимаем на «Разрешить».\nПодтверждаем добавление карты в Apple Wallet и нажимаем «Добавить».')
        await callback.message.answer('Готово!\n\nКак зарегистрируетесь, возвращайтесь в чат и жмите «Готово!», чтобы дополнительно получить 300 бонусных рублей на ваш счёт! ↓',
            reply_markup=how_kb())
    except: pass

#About
@router.message(Text('✍️ О нас'))
async def menu(message: Message):
    try:
        await message.answer(
            'Что вы хотели узнать о нас?', reply_markup=about_kb()
        )
    except: pass

#Maps
@router.callback_query(Text('reviews'))
async def change_contact(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚩 Мы на Яндекс Картах", 
        url="https://yandex.ru/maps/org/hookahplace_life/143683058547?si=dv8cwb3uyqueubzqfbuf71a080"
        )
    try:
        await callback.message.answer("Мы одни из лучших заведений в городе, что подтверждает наш высокий рейтинг на картах.\n\nИ всегда стремимся к тому, чтобы каждый гость чувствовал себя как дома и качественно отдыхал в нашем заведении!\n\nПриходите к нам и убедитесь сами!",
            reply_markup=builder.as_markup(resize_keyboard=True))
    except: pass

#Where
@router.callback_query(Text('where'))
async def change_contact(callback: CallbackQuery):
    try:
        await bot.send_chat_action(chat_id=callback.from_user.id, action=ChatAction.UPLOAD_VIDEO)
        await callback.message.answer_video(FSInputFile('where.MP4'), width=720, height=1280, caption='📍 Наш адрес: Каширский проезд, 25, корп. 2')
    except: pass

#About text
@router.callback_query(Text('about'))
async def change_contact(callback: CallbackQuery):
    try:
        await callback.message.answer("Мы HookahPlace Life — ваши проводники в кальянную культуру.\n\nМы верим, что кальян — это опыт, которым мы готовы делиться с вами. Мы предлагаем уникальные ароматы, выходящие за пределы традиционных сочетаний.\n\nПомимо кальяна, у нас вы сможете насладиться традиционным китайским чаем, каждый пролив которого — медитация. В чайной церемонии важно всё: от выбора посуды до температуры воды и времени настаивания.\n\nМы с нетерпением ждем вас! Загляните к нам и откройте новые горизонты впечатлений!\n\nПриглашаем вас погрузиться в атмосферу спокойствия и гармонии.")
    except: pass

#SM
@router.callback_query(Text('sm'))
async def change_contact(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🗣️ VK", 
        url="https://vk.com/hookahplace.life"
        )
    builder.button(
        text="📷 INST*", 
        url="https://www.instagram.com/hookahplace.life?igsh=MW1qenJqOWZkdXU5eA=="
        )
    builder.button(
        text="🌍 Сайт", 
        url="https://hplife.ru"
        )
    builder.adjust(1)
    try:
        await callback.message.answer(f'Мы в социальных сетях:\n\n*Деятельность Meta (соцсети Facebook и Instagram) запрещена в России как экстремистская.', reply_markup=builder.as_markup(resize_keyboard=True))
    except: pass

#admin

async def broadcast_message(users_data: list, text: str = None, photo_id: int = None, document_id: int = None,
                            video_id: int = None, audio_id: int = None, caption: str = None, content_type: str = None, sender_name: str = None):
    good_send = 0
    bad_send = 0
    for user in users_data:
        try:
            chat_id = user[0]
            if content_type == ContentType.TEXT:
                await bot.send_message(chat_id=chat_id, text=text)
            elif content_type == ContentType.PHOTO:
                await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption)
            elif content_type == ContentType.DOCUMENT:
                await bot.send_document(chat_id=chat_id, document=document_id, caption=caption)
            elif content_type == ContentType.VIDEO:
                await bot.send_video(chat_id=chat_id, video=video_id, caption=caption)
            elif content_type == ContentType.AUDIO:
                await bot.send_audio(chat_id=chat_id, audio=audio_id, caption=caption)
            good_send += 1
        except Exception as e:
            print(e)
            bad_send += 1
        finally:
            await asyncio.sleep(1)
    for user in db.get_admins_id():
        try:
            chat_id = user
            if content_type == ContentType.TEXT:
                await bot.send_message(chat_id=chat_id, text=text+'\n(написал(а) '+sender_name+')')
            elif content_type == ContentType.PHOTO:
                await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption)
            elif content_type == ContentType.DOCUMENT:
                await bot.send_document(chat_id=chat_id, document=document_id, caption=caption)
            elif content_type == ContentType.VIDEO:
                await bot.send_video(chat_id=chat_id, video=video_id, caption=caption)
            elif content_type == ContentType.AUDIO:
                await bot.send_audio(chat_id=chat_id, audio=audio_id, caption=caption)
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(1)
    return good_send, bad_send


@router.message(Command(commands=["admin"]))
async def cmd_all(message: Message):
    if message.from_user.id in db.get_admins_id():
        try:
            await message.answer(
                'Список команд администратора', reply_markup=admin_kb(message.from_user.id)
            )
        except: pass

@router.callback_query((F.from_user.id in db.get_admins_id()) & (F.data == 'admin_users'))
async def admin_users_handler(callback: CallbackQuery):
    text = "Список пользователей\n\n"
    users = db.get_users()
    text_active = '✅ Активировали карту (за N дней):\n'
    text_try_active = '❓ Пытались активировать карту (N дней):\n'
    text_ntry_active = '❌ Не пытались активировать карту:\n'
    for i in users:
        if db.user_tryed(i[0]):
            if db.user_active(i[0]):
                text_active += f'<a href="tg://openmessage?user_id={i[0]}">{i[1]}</a> ('+str(db.get_day(i[0]))+')\n'
            else:
                text_try_active += f'<a href="tg://openmessage?user_id={i[0]}">{i[1]}</a> ('+str(db.get_day(i[0]))+')\n'
        else:
            text_ntry_active += f'<a href="tg://openmessage?user_id={i[0]}">{i[1]}</a>\n'
    text += '\n' + text_active + '\n' + text_try_active + '\n' + text_ntry_active + '\nВсего пользователей: ' + str(len(users))
    try:
        await callback.message.answer(text, reply_markup=admin_kb(callback.from_user.id), disable_web_page_preview=True, parse_mode="HTML")
    except: pass

@router.callback_query((F.from_user.id in db.get_admins_id()) & (F.data == 'admin_broadcast'))
async def admin_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправьте любое сообщение, а я его перехвачу и перешлю всем пользователям бота',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.start_broadcast)

@router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio'}), Form.start_broadcast)
async def universe_broadcast(message: Message, state: FSMContext):
    users_data = db.get_users()

    # Определяем параметры для рассылки в зависимости от типа сообщения
    content_type = message.content_type

    if content_type == ContentType.TEXT and message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Рассылка отменена!', reply_markup=get_user_kb())
        return

    await message.answer(f'Начинаю рассылку на {len(users_data)} пользователей.')

    good_send, bad_send = await broadcast_message(
        users_data=users_data,
        text=message.text if content_type == ContentType.TEXT else None,
        photo_id=message.photo[-1].file_id if content_type == ContentType.PHOTO else None,
        document_id=message.document.file_id if content_type == ContentType.DOCUMENT else None,
        video_id=message.video.file_id if content_type == ContentType.VIDEO else None,
        audio_id=message.audio.file_id if content_type == ContentType.AUDIO else None,
        caption=message.caption,
        content_type=content_type,
        sender_name=message.from_user.first_name+' всем'
    )

    await state.clear()
    await message.answer(f'Рассылка завершена. Сообщение получило {good_send}, '
                         f'НЕ получило {bad_send} пользователей.', reply_markup=get_user_kb())

#broad not active
@router.callback_query((F.from_user.id in db.get_admins_id()) & (F.data == 'admin_broadcast_not_active'))
async def admin_broadcast_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Отправьте любое сообщение, а я его перехвачу и перешлю только тем, кто не активировал карту лояльности',
        reply_markup=cancel_btn()
    )
    await state.set_state(Form.start_broadcast_not_active)

@router.message(F.content_type.in_({'text', 'photo', 'document', 'video', 'audio'}), Form.start_broadcast_not_active)
async def universe_broadcast(message: Message, state: FSMContext):
    users_data = db.get_not_active_users()

    # Определяем параметры для рассылки в зависимости от типа сообщения
    content_type = message.content_type

    if content_type == ContentType.TEXT and message.text == '❌ Отмена':
        await state.clear()
        await message.answer('Рассылка отменена!', reply_markup=get_user_kb())
        return

    await message.answer(f'Начинаю рассылку на {len(users_data)} пользователей.')

    good_send, bad_send = await broadcast_message(
        users_data=users_data,
        text=message.text if content_type == ContentType.TEXT else None,
        photo_id=message.photo[-1].file_id if content_type == ContentType.PHOTO else None,
        document_id=message.document.file_id if content_type == ContentType.DOCUMENT else None,
        video_id=message.video.file_id if content_type == ContentType.VIDEO else None,
        audio_id=message.audio.file_id if content_type == ContentType.AUDIO else None,
        caption=message.caption,
        content_type=content_type,
        sender_name=message.from_user.first_name+' всем нелояльным'
    )

    await state.clear()
    await message.answer(f'Рассылка завершена. Сообщение получило {good_send}, '
                         f'НЕ получило {bad_send} пользователей.', reply_markup=get_user_kb())

#Добавить
@router.callback_query((F.from_user.id in admins) & (F.data == 'add_admin'))
async def admin_broadcast_handler(call: CallbackQuery):
    await call.message.answer(
        'Выберите человека, которого вы хотите назначить админом. Он должен быть в базе данных, пусть отправит /start боту если он еще не подписан на него', reply_markup=add_admin_kb())

@router.message(F.user_shared)
async def handle_user(message: Message):
    try:
        db.set_admin(message.user_shared.user_id)
        await message.answer(f'<a href="tg://openmessage?user_id={message.user_shared.user_id}">Админ</a> назначен', reply_markup=get_user_kb(), disable_web_page_preview=True, parse_mode="HTML")
    except:
        await message.answer(f'<a href="tg://openmessage?user_id={message.user_shared.user_id}">Пользователя</a> нет в базе данных, пусть отправит /start боту', reply_markup=get_user_kb(), disable_web_page_preview=True, parse_mode="HTML")

@router.message(Text('❌ Отмена'))
async def menu(message: Message):
    try:
        await message.answer(
            'Команда отменена', reply_markup=get_user_kb()
        )
    except: pass

@router.callback_query((F.from_user.id in admins) & (F.data == 'admin_list'))
async def admin_broadcast_handler(call: CallbackQuery):
    list = 'Список админов:\n\n'
    count = 1
    for i in db.get_admins():
        if i[0] not in admins:
            list += str(count) + f') <a href="tg://openmessage?user_id={i[0]}">{i[1]}</a>\n'
            count += 1
    await call.message.answer(list, disable_web_page_preview=True, parse_mode="HTML")

#Удалить
class AdminsCallbackFactory(CallbackData, prefix="fabad"):
    id: str

@router.callback_query((F.from_user.id in admins) & (F.data == 'del_admin'))
async def admin_broadcast_handler(call: CallbackQuery):
    list = 'Список админов:\n\n'
    count = 1
    builder = InlineKeyboardBuilder()
    for i in db.get_admins():
        if i[0] not in admins:
            list += str(count) + f') <a href="tg://openmessage?user_id={i[0]}">{i[1]}</a>\n'
            builder.button(text = str(count)+') '+i[1], 
                    callback_data=AdminsCallbackFactory(id = i[0]))
            count += 1
    builder.button(text='❌ Отмена', callback_data='cancel')
    builder.adjust(1)
    await call.message.answer(
        'Выберите человека, которого вы хотите удалить из админов\n'+list, reply_markup=builder.as_markup(resize_keyboard=True), disable_web_page_preview=True, parse_mode="HTML")

@router.callback_query(AdminsCallbackFactory.filter())
async def add_laundry_sentry_fab(callback: CallbackQuery, callback_data: AdminsCallbackFactory):
    await callback.message.delete()
    try:
        db.del_admin(callback_data.id)
        await callback.message.answer(f'<a href="tg://openmessage?user_id={callback_data.id}">Пользователь</a> больше не обладает правами администратора', disable_web_page_preview=True, parse_mode="HTML")
    except:
        await callback.message.answer(f'<a href="tg://openmessage?user_id={callback_data.id}">Пользователь</a> не обладал правами администратора', disable_web_page_preview=True, parse_mode="HTML")

@router.callback_query(Text('cancel'))
async def cancel(callback: CallbackQuery):
    await callback.message.answer(
            text='Команда отменена')
    await callback.message.delete()

#Unknown
@router.message()
async def error(message: Message):
    try:
        await message.answer(
            "Простите, я вас не понимаю"
        )
    except: pass