from aiogram import executor
from createBot import dp
from handlers.admin import register_handlers_admin
from handlers.client import register_handlers_client


async def on_startup(_):
    print('Бот успешно запущен!')

register_handlers_admin(dp)
register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)