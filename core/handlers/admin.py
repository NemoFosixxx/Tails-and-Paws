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


class admin_class():
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
            await callback_query.message.answer("Какой добавить текст для кнопки?", reply_markup=None)
            await state.set_state(SenderSteps.GET_TEXT_BUTTON)
        elif callback_query.data == 'no_button':
            # здесь должен быть вызов функции
            await state.set_state(SenderSteps.Q_IMAGE)

    async def get_text_button(message: Message, state: FSMContext):
        await state.update_data(text_button=message.text)
        await message.answer("Какая ссылка будет у кнопки?")
        await state.set_state(SenderSteps.GET_URL_BUTTON)

    async def get_url_button(message: Message, state: FSMContext):
        # IF GET.DATA(TEXT_BUTTON) != NONE
        await state.update_data(url_button=message.text)
        await message.answer("Я сохранил вашу кнопку!")
        # здесь должен быть вызов функции
        await state.set_state(SenderSteps.Q_IMAGE)

    async def q_image(message: Message, state: FSMContext):
        await message.answer("Добавлять ли изображение?", reply_markup=inline_get_image_keyboard())

    async def get_image(self, callback_query: types.CallbackQuery, state: FSMContext):
        if callback_query.data == 'add_image':
            await callback_query.message.answer("Отправьте изображение, которое нужно прикрепить к рассылке")
            await state.set_state(SenderSteps.GET_FILE_IMAGE)
        elif callback_query.data == 'no_image':
            data = await state.get_data()
            message_text = str(data.get('message_text'))
            user_id = int(data.get('user_id'))
            text_button = str(data.get('text_button', None))
            url_button = str(data.get('url_button', None))
            self.confirm(message_text, user_id, text_button, url_button)

    async def get_file_image(self, message: Message, state: FSMContext, bot: Bot):
        file = await bot.get_file(message.photo[-1].file_id)
        await state.update_data(photo=bot.download_file(file.file_path, 'core\images\image_sender\image.jpg'))

        data = await state.get_data()
        photo = data.get('photo')
        message_text = str(data.get('message_text'))
        user_id = int(data.get('user_id'))
        text_button = str(data.get('text_button', None))
        url_button = str(data.get('url_button', None))
        self.confirm(photo, message_text, user_id, text_button, url_button)

    async def confirm(self, message: Message, state: FSMContext, bot: Bot, photo: None, message_text: str, user_id: int, text_button: None, url_button: None):
        # photo = FSInputFile(r'core\images\image_sender\image.jpg')
        # data = await state.get_data()
        # photo = data.get('photo')
        # message_text = str(data.get('message_text'))
        # user_id = int(data.get('user_id'))
        # text_button = str(data.get('text_button', None))
        # url_button = str(data.get('url_button', None))
        if text_button is not None:  # Если кнопка существует
            added_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=text_button, url=url_button)
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
        await message.answer("Вот ваш итоговый текст. Опубликовать рассылку", reply_markup=inline_sender_keyboard)

    # added_keyboards = InlineKeyboardMarkup(inline_keyboard=[
    #     [
    #         InlineKeyboardButton(text=(await state.get_data()).get('text_button'),
    #                              url=f'{message.text}'
    #                              )
    #     ]
    # ])
    # await state.update_data(keyboard=added_keyboards)
    # Добавить FSM

    # async def get_image(message: types.Message, bot: Bot, state: FSMContext):
    # data = await state.get_data()
    # message_id = int(data.get('message_id'))              ВСЁ В ДРУГУЮ В ОКОНЧАТЕЛЬНУЮ ФУНКЦИЮ
    # chat_id = int(data.get('chat_id'))
    # added_keyboards = (data.get('added_keyboards')) # работает ли? СДЕЛАТЬ БИЛДЕРОМ + РЕТУРНОМ (ВЫНЕСТИ В МЕТОД)
    # await self.confirm(message, bot, message_id, chat_id, added_keyboards)

    # await message.answer("Добавлять ли картинку?", reply_markup=inline_get_image_keyboard())
    # await state.set_state(SenderSteps.Q_IMAGE)
    # file = await bot.get_file(message.photo[-1].file_id)
    # await bot.download_file(file.file_path, 'core\images\image.png')

        # await self.get_image(callback_query.message, bot, message_id, chat_id, )

    # async def confirm(self, message: Message, bot: Bot, message_id: int, chat_id: int, reply_markup: InlineKeyboardMarkup = None, photo: FSInputFile = None):
    #     # Копируется сообщение, добавляется кнопка, при наличии и отправляется админу
    #     await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)
    #     await message.answer(f'Вот сообщение, которое будет отправлено: \n Подтверди.', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
    #         [
    #             InlineKeyboardButton(
    #                 text='Подтвердить', callback_data='confirm_sender'
    #             )
    #         ],
    #         [
    #             InlineKeyboardButton(
    #                 text='Отклонить', callback_data='decline_sender'
    #             )
    #         ]
    #     ]))

    async def sender_decide(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))
        text_button = data.get("text_button")
        url_button = data.get("button_url")

        if callback_query.data == 'confirm_sender':
            await callback_query.message.edit_text('Начинаю рассылку', reply_markup=None)
        elif callback_query.data == 'decline_sender':
            await callback_query.message.edit_text('Отменил рассылку', reply_markup=None)

        await state.clear()

        # added_keyboards = InlineKeyboardMarkup(inline_keyboard=[
        #     [
        #         InlineKeyboardButton(text=(await state.get_data()).get('text_button'),
        #                              url=f'{message.text}'
        #                              )
        #     ]
        # ])
