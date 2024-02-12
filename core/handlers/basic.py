from aiogram import Bot, types, Dispatcher
from aiogram.types import Message, FSInputFile
from core.settings import settings
from core.keyboards.inline import inline_start_keyboard, inline_buy_info_keyboard
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

    async def buy(callback_query: types.CallbackQuery, bot: Bot):
        await callback_query.message.answer("Добро пожаловать на курс по правильному обращению с домашними животными! Наша программа разработана с учетом многообразия видов и разновидностей домашних питомцев, предоставляя участникам уникальную возможность углубить свои знания в эффективных методах обучения, понимания потребностей, ухода и коммуникации с любимыми домашними друзьями. \n\nВ течение курса вы познакомитесь с основами психологии животных, общими принципами ухода и обучения, а также освоите технику воспитания. Наша цель - помочь вам стать настоящим экспертом в области обращения с домашними животными, обеспечивая полноценное и гармоничное взаимодействие с вашими питомцами. Присоединяйтесь к нам и открывайте мир дружбы и взаимопонимания с животными!",
                                            reply_markup=inline_buy_info_keyboard())

    async def buy_info_back(callback_query: types.CallbackQuery):
        await callback_query.message.delete()
