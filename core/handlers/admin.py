from aiogram import Bot, types, Dispatcher
from aiogram.types import Message, FSInputFile
from core.settings import settings
from core.utils import sqlite
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm, SenderSteps
from aiogram.filters import CommandObject
from core.keyboards.inline import inline_admin_keyboard, inline_get_buttons_keyboard, inline_get_image_keyboard, inline_sender_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputFile


async def admin_panel(message: types.Message, bot: Bot):
    await message.answer("✅Включён режим администратора✅",
                         reply_markup=inline_admin_keyboard())


async def get_profile(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback_query.from_user.id == settings.bots.admin_id or settings.bots.base_admin_id:
        await callback_query.message.answer("Перешлите сообщение от пользователя мне. Я внесу его в список пользователей, которые купили курс.")
        await state.set_state(StepsForm.GET_FORWARDS_MESSAGE)


async def upgrade_profile(message: types.Message, state: FSMContext, bot: Bot):
    await sqlite.upgrade_profile(user_id=message.forward_from.id, username=message.forward_from.username)
    await message.answer("Пользователь успешно внесён в базу данных курса✅")
    await state.clear()

# РАССЫЛКА СООБЩЕНИЙ


async def get_sender(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Отправьте мне текст для рассылки")
    await state.set_state(SenderSteps.GET_MESSAGE)


async def get_message(message: Message, state: FSMContext):
    # сохраняет id отправителя и текст сообщения
    await state.update_data(message_text=message.text, user_id=message.from_user.id)
    await message.answer("Отлично, я запомнил ваш текст!  Добавлять ли кнопки?", reply_markup=inline_get_buttons_keyboard())


async def q_button(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'add_button':
        await callback_query.message.answer("Какой добавить текст для кнопки?")
        await state.set_state(SenderSteps.GET_TEXT_BUTTON)
    elif callback_query.data == 'no_button':
        # здесь должен быть вызов функции

        await q_image(callback_query.message)


async def get_text_button(message: Message, state: FSMContext):
    await state.update_data(text_button=message.text)
    await message.answer("Какая ссылка будет у кнопки?")
    await state.set_state(SenderSteps.GET_URL_BUTTON)


async def get_url_button(message: Message, state: FSMContext, bot: Bot):
    # IF GET.DATA(TEXT_BUTTON) != NONE
    await state.update_data(url_button=message.text)
    message = 'Добавлять ли изображение?'
    await q_image(state, bot, message)


async def q_image(state: FSMContext, bot: Bot, message):
    data = await state.get_data()
    user_id = int(data.get('user_id'))
    await bot.send_message(user_id, message, reply_markup=inline_get_image_keyboard())


async def get_image(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'add_image':
        await callback_query.message.answer("Отправьте изображение, которое нужно прикрепить к рассылке")
        await state.set_state(SenderSteps.GET_FILE_IMAGE)
    elif callback_query.data == 'no_image':
        data = await state.get_data()
        message_text = str(data.get('message_text'))
        user_id = int(data.get('user_id'))
        text_button = str(data.get('text_button', None))
        url_button = str(data.get('url_button', None))
        await confirm(message_text, user_id, text_button, url_button)


async def get_file_image(message: Message, state: FSMContext, bot: Bot):
    if message.photo is not None and len(message.photo) > 0:
        file = await bot.get_file(message.photo[-1].file_id)
        photo_path = 'core\images\image_sender\image.jpg'
        await bot.download_file(file.file_path, photo_path)
        photo = FSInputFile(photo_path)

        data = await state.get_data()
        message_text = str(data.get('message_text'))
        user_id = int(data.get('user_id'))
        text_button = str(data.get('text_button', None))
        url_button = str(data.get('url_button', None))

        await confirm(message, state, bot, photo, message_text, user_id, text_button, url_button)
    else:
        message.answer(
            "Случилась какая-то ошибка и фотография не была получена. Попробуйте сначала.")


async def confirm(message: Message, state: FSMContext, bot: Bot, photo, message_text, user_id: int, text_button, url_button: str):
    if text_button is not None:  # Если кнопка существует
        added_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=(await state.get_data()).get('text_button'), url=f'{url_button}')
            ]
        ])

        if photo is not None:  # Если фото существует

            await bot.send_photo(user_id, photo, caption=message_text, reply_markup=added_keyboard)
        else:
            await bot.send_message(user_id, message_text, reply_markup=added_keyboard)

    elif text_button is None:  # Если кнопки не существует
        if photo is not None:  # Если фото существует
            await bot.send_photo(user_id, photo, caption=message_text)
        elif photo is None:
            await bot.send_message(user_id, message_text)

    add_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Опубликовать',
                                 callback_data='accept_sender')
        ],
        [
            InlineKeyboardButton(
                text='Отменить рассылку', callback_data='decline_sender')
        ]
    ])
    await message.answer("Вот ваш итоговый текст. Опубликовать рассылку?", reply_markup=add_keyboard)
    await state.clear()
