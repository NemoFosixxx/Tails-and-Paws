from aiogram import Bot, types, Dispatcher
from aiogram.types import Message, FSInputFile
from core.settings import settings
from core.utils import sqlite
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm, SenderSteps
from aiogram.filters import CommandObject
from core.keyboards.inline import inline_admin_keyboard, inline_get_buttons_keyboard, inline_get_image_keyboard
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

    async def get_sender(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
        if callback_query.from_user.id == settings.bots.admin_id or settings.bots.base_admin_id:
            await callback_query.message.answer("Приступаем создавать рассылку. Отправь мне сообщение, которое будет использоваться")
            await state.set_state(SenderSteps.GET_MESSAGE)

    async def get_message(message: types.Message, state: FSMContext):
        await message.answer("Я запомнил твоё сообщение. \nДобавлять ли мне кнопку?",
                             reply_markup=inline_get_buttons_keyboard())
        await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
        await state.set_state(SenderSteps.Q_BUTTON)

    async def q_button(self, callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
        if callback_query.data == 'add_button':
            await callback_query.message.answer('Отправь текст для кнопки', reply_markup=None)
            await state.set_state(SenderSteps.GET_BUTTON)
        elif callback_query.data == 'no_button':
            await callback_query.message.edit_reply_markup(None)
            data = await state.get_data()
            message_id = int(data.get('message_id'))
            chat_id = int(data.get('chat_id'))
            await self.get_image(callback_query.message, bot, message_id, chat_id)
            # ДОБАВИТЬ FSM
        # вызов функции подтверждения

    async def get_text_button(self, message: types.Message, bot: Bot, state: FSMContext):
        await state.update_data(text_button=message.text)
        await message.answer("Теперь отправь ссылку для кнопки")
        await state.set_state(SenderSteps.GET_URL_BUTTON)

    async def get_url_button(self, message: Message, state: FSMContext, bot: Bot):
        await state.update_data(button_url=message.text)
        # added_keyboards = InlineKeyboardMarkup(inline_keyboard=[
        #     [
        #         InlineKeyboardButton(text=(await state.get_data()).get('text_button'),
        #                              url=f'{message.text}'
        #                              )
        #     ]
        # ])
        # await state.update_data(keyboard=added_keyboards)
        # Добавить FSM

    async def get_image(message: types.Message, bot: Bot, state: FSMContext):
        # data = await state.get_data()
        # message_id = int(data.get('message_id'))              ВСЁ В ДРУГУЮ В ОКОНЧАТЕЛЬНУЮ ФУНКЦИЮ
        # chat_id = int(data.get('chat_id'))
        # added_keyboards = (data.get('added_keyboards')) # работает ли? СДЕЛАТЬ БИЛДЕРОМ + РЕТУРНОМ (ВЫНЕСТИ В МЕТОД)
        # await self.confirm(message, bot, message_id, chat_id, added_keyboards)
        await message.answer("Добавлять ли картинку?", reply_markup=inline_get_image_keyboard())
        await state.set_state(SenderSteps.Q_IMAGE)
        # file = await bot.get_file(message.photo[-1].file_id)
        # await bot.download_file(file.file_path, 'core\images\image.png')

    async def q_image(self, callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
        if callback_query.data == 'add_image_sender':
            await callback_query.message.answer(
                "Хорошо! Теперь отправь изображение, которое нужно прикрепить к рассылке")
            await state.set_state(SenderSteps.GET_IMAGE)
        elif callback_query == 'no_image_sender':
            await callback_query.message.edit_reply_markup(None)
            data = await state.get_data()
            message_id = int(data.get('message_id'))
            chat_id = int(data.get('chat_id'))
            await self.get_image(callback_query.message, bot, message_id, chat_id, )

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
