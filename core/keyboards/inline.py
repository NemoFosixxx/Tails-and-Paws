from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# def get_inline_keyboard():
#     keyboard_builder = InlineKeyboardBuilder()
#     keyboard_builder.button(text='Звёздочку', callback_data='add_star')
#     keyboard_builder.button(text='Картинку', callback_data='add_image')

#     return keyboard_builder.as_markup()

def inline_start_keyboard():
    start_inline_builder = InlineKeyboardBuilder()
    start_inline_builder.button(text="Купить (О нас)",
                                callback_data='buy_info')
    start_inline_builder.button(text="Наш новостной канал",
                                url='https://t.me/HvostiiLapi')
    start_inline_builder.button(text="Помощь",
                                url='https://t.me/KseniaKiz')
    start_inline_builder.adjust(1, 2)

    return start_inline_builder.as_markup()


def inline_buy_info_keyboard():
    buy_info_inline_builder = InlineKeyboardBuilder()
    buy_info_inline_builder.button(
        text="Связаться для оплаты", url='https://t.me/KseniaKiz')
    buy_info_inline_builder.button(text="Назад",
                                   callback_data='buy_back')
    buy_info_inline_builder.adjust(1, 2)

    return buy_info_inline_builder.as_markup()


def inline_admin_keyboard():
    admin_inline_builder = InlineKeyboardBuilder()
    admin_inline_builder.button(
        text='Апгрейд пользователя', callback_data='upgrade_user')
    admin_inline_builder.button(
        text='Удаление пользователя', callback_data='delete_user')
    admin_inline_builder.button(
        text='Рассылка сообщений', callback_data='sender')

    admin_inline_builder.adjust(2, 1)
    return admin_inline_builder.as_markup()


def inline_back_admin_keyboard():
    back_admin_inline_keyboard = InlineKeyboardBuilder()
    back_admin_inline_keyboard.button(text='Назад', callback_data='back_admin')

    back_admin_inline_keyboard.adjust(1)
    return back_admin_inline_keyboard.as_markup()


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
        text='Да, добавить', callback_data='add_image')
    get_image_inline_keyboard.button(
        text='Нет, не добавлять', callback_data='no_image')
    get_image_inline_keyboard.adjust(2)
    return get_image_inline_keyboard.as_markup()


def inline_send_to_upgrade_user_keyboard():  # При покупке пользователем курса.
    send_upgrade_user_keyboard = InlineKeyboardBuilder()
    send_upgrade_user_keyboard.button(
        text="Начать!", callback_data='upgrade_user_start')  # Здесь должна быть reply кнопка
    send_upgrade_user_keyboard.adjust(1)

    return send_upgrade_user_keyboard.as_markup()
