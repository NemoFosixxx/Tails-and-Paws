from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# def get_inline_keyboard():
#     keyboard_builder = InlineKeyboardBuilder()
#     keyboard_builder.button(text='Звёздочку', callback_data='add_star')
#     keyboard_builder.button(text='Картинку', callback_data='add_image')

#     return keyboard_builder.as_markup()

def inline_start_keyboard():
    start_inline_builder = InlineKeyboardBuilder()
    start_inline_builder.button(text="Оплата",
                                url="https://t.me/KseniaKiz")
    start_inline_builder.button(text="Наш новостной канал",
                                url='https://t.me/HvostiiLapi')
    start_inline_builder.button(text="Помощь",
                                url='https://t.me/KseniaKiz')
    start_inline_builder.adjust(1, 2)

    return start_inline_builder.as_markup()


def inline_admin_keyboard():
    admin_inline_builder = InlineKeyboardBuilder()
    admin_inline_builder.button(
        text='Апгрейд пользователя', callback_data='upgrade_user')
    admin_inline_builder.button(
        text='Рассылка сообщений', callback_data='sender')

    admin_inline_builder.adjust(1, 1)
    return admin_inline_builder.as_markup()


def inline_get_buttons_keyboard():
    get_buttons_inline_keyboard = InlineKeyboardBuilder()
    get_buttons_inline_keyboard.button(
        text="Да, добавить", callback_data="add_button")
    get_buttons_inline_keyboard.button(
        text='Нет, не добавлять', callback_data="no_button")
    get_buttons_inline_keyboard.adjust(2)
    return get_buttons_inline_keyboard.as_markup()


def inline_get_image_keyboard():
    get_image_inline_keyboard = InlineKeyboardBuilder()
    get_image_inline_keyboard.button(
        text='Да, добавить', callback_data='add_image_sender')
    get_image_inline_keyboard.button(
        text='Нет, не добавлять', callback_data='no_image_sender')
    get_image_inline_keyboard.adjust(2)
    return get_image_inline_keyboard.as_markup()
