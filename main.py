import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from core.settings import settings
from core.handlers.basic import basic_class
from core.handlers.admin import admin_class
from core.utils.statesform import StepsForm, SenderSteps
from aiogram.methods import DeleteWebhook

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bots.bot_token,
          parse_mode='HTML')

dp = Dispatcher()

# Включение и выключение бота


async def main():
    bot = Bot(token=settings.bots.bot_token,
              parse_mode='HTML')

    dp = Dispatcher()

# handlers

    dp.startup.register(basic_class.start_bot)
    dp.shutdown.register(basic_class.stop_bot)
    dp.message.register(basic_class.cmd_start, Command("start"))
    dp.message.register(admin_class.admin_panel, Command(
        "admin"), F.chat.id == settings.bots.admin_id or settings.bots.base_admin_id)
    dp.callback_query.register(
        admin_class.get_profile, F.data == "upgrade_user")
    dp.message.register(admin_class.upgrade_profile,
                        StepsForm.GET_FORWARDS_MESSAGE)
    dp.callback_query.register(admin_class.get_sender, F.data == 'sender')
    dp.message.register(admin_class.get_message, SenderSteps.GET_MESSAGE)
    dp.callback_query.register(
        admin_class.q_button, F.data == 'add_button' or 'no_button')
    dp.message.register(admin_class.get_text_button,
                        SenderSteps.GET_TEXT_BUTTON)
    dp.message.register(admin_class.get_url_button, SenderSteps.GET_URL_BUTTON)
    dp.message.register(admin_class.q_image, SenderSteps.Q_IMAGE)
    dp.callback_query.register(
        admin_class.get_image, F.data == 'add_image' or 'no_image')
    dp.message.register(admin_class.get_file_image, SenderSteps.GET_FILE_IMAGE)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == "__main__":
    asyncio.run(main())
    # bot(DeleteWebhook(drop_pending_updates=True))
    # dp.start_polling(bot)
