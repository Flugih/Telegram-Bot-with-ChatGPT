from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def create_pay_button(link):
    pay_buttons = (
        InlineKeyboardButton('Купить подписку', url=link),
    )

    check_pay = (
        InlineKeyboardButton('Проверить платеж', callback_data='check_payment'),
    )

    pay_button = ReplyKeyboardMarkup()
    pay_button = InlineKeyboardMarkup().add(*pay_buttons).add(*check_pay)
    return pay_button


buttons = (
    KeyboardButton('❗ Поддержка'),
    KeyboardButton('ℹ Помощь'),
)

buttons2 = (
    KeyboardButton('👤 Профиль'),
)

buy_buttons = (
    InlineKeyboardButton('Купить VIP', callback_data='buy_vip'),
)

sup_buttons = (
    InlineKeyboardButton('Написать в поддержку', callback_data='write_to_sup'),
)


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
sup_button = ReplyKeyboardMarkup()
buy_button = ReplyKeyboardMarkup()

kb_client.add(*buttons).add(*buttons2)

buy_button = InlineKeyboardMarkup().add(*buy_buttons)
sup_button = InlineKeyboardMarkup().add(*sup_buttons)