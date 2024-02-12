from aiogram import Bot, types, Dispatcher
from aiogram.types import Message, FSInputFile
from core.settings import settings
# from core.keyboards.inline import inline_start_keyboard, inline_buy_info_keyboard
from core.utils import sqlite
# from core.utils.sqlite import check_user_exist

# async def first_lesson():


async def first_homework(callback_query: types.CallbackQuery, bot: Bot):

    # user_exists = await sqlite.check_user_exist(user_id=callback_query.message.from_user.id)
    # if user_exists == True:
    #     await callback_query.message.answer('Привет, чтобы подытожить твои знания, давай пройдём опрос!')
    #     callback_query.message.answer_poll(question='Что нельзя есть кошкам?',
    #                                        options=[
    #                                            'Мясо', 'Морковь и огурец', 'Кефир', 'Рис и гречку', 'Лук и чеснок', 'Кабачки и тыква'],
    #                                        correct_option_id=4,
    #                                        explanation='На самом деле им нельзя есть лук и чеснок',
    #                                        is_anonymous=True,
    #                                        allows_multiple_answers=False)
    # else:
    #     callback_query.message.answer(
    #         "Вы ещё не купили курс, чтобы использовать эту команду!")
    await callback_query.message.answer('Привет, чтобы подытожить твои знания, давай пройдём опрос!')
    await callback_query.message.answer_poll(question='Что нельзя есть кошкам?',
                                             options=[
                                                 'Мясо', 'Морковь и огурец', 'Кефир', 'Рис и гречку', 'Лук и чеснок', 'Кабачки и тыква'],
                                             correct_option_id=4,
                                             explanation='На самом деле им нельзя есть лук и чеснок',
                                             type='quiz',
                                             is_anonymous=True,
                                             allows_multiple_answers=False)
