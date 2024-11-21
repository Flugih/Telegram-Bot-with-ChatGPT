from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

delete_callback = CallbackData('delete', 'message_id')

buttons = (
    InlineKeyboardButton('Готово', callback_data='remove'),
)

sup_confirm_button = ReplyKeyboardMarkup()
sup_confirm_button = InlineKeyboardMarkup().add(*buttons)