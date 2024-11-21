from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

buttons1 = (
    KeyboardButton('Рассылка'),
    KeyboardButton('Статистика бота'),
    KeyboardButton('Сообщение юзеру'),
)

buttons2 = (
    KeyboardButton('Назад'),
)

statistics_buttons = (
    InlineKeyboardButton('Очистить запросы', callback_data='clear_requests'),
)

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
statistic_button = ReplyKeyboardMarkup()

kb_admin.add(*buttons1)
kb_admin.add(*buttons2)
statistic_button = InlineKeyboardMarkup().add(*statistics_buttons)
