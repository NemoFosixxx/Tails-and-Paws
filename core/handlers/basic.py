from aiogram import Bot, types, Dispatcher
from aiogram.types import Message, FSInputFile
from core.settings import settings
from core.keyboards.inline import inline_start_keyboard
from core.utils import sqlite


class basic_class():

    async def start_bot(bot: Bot):
        await bot.send_message(settings.bots.admin_id, f'✅<b>Бот был включён!</b>✅')
        await sqlite.db_start()
        await bot.send_message(settings.bots.admin_id, "База данных была подгружена!")

    async def stop_bot(bot: Bot):
        await bot.send_message(settings.bots.admin_id, f'❌<b>Бот был остановлен!</b>❌')

    async def cmd_start(message: Message, bot: Bot):
        photo = FSInputFile(r'core\images\start_image.jpg')
        await bot.send_photo(message.chat.id, photo, caption="Привет, я бот, через которого ты можешь узнать о том, как ухаживать за животными!",
                             reply_markup=inline_start_keyboard())
        await sqlite.create_profile(user_id=message.from_user.id, username=message.from_user.username)


# Здесь должны быть кнопки
