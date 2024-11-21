from aiogram import types, Dispatcher, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from createBot import bot
import DB
import keyboards


class FSMAdmin(StatesGroup):
    msg = State()

class MSGforUser(StatesGroup):
    chat_id = State()
    msg = State()


async def admin_mailing(message: types.Message):
    await FSMAdmin.msg.set()
    await bot.send_message(message.from_user.id, 'Введите сообщение для рассылки')


async def send_mailing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    await bot.send_message(message.from_user.id, 'Рассылка успешно запущена!')

    async with state.proxy() as data:
        last_id = DB.get_last_id()
        for user_id in range(last_id):
            user_id += 1
            chat_id = DB.get_chat_id(user_id)
            await bot.send_message(chat_id=chat_id, text=f'{data["msg"]}')
    await state.finish()


async def bot_statistic(message: types.Message):
    last_id = DB.get_last_id()
    all_requests = 0
    for user_id in range(last_id):
        user_id += 1
        all_requests += DB.get_requests(user_id)
    await bot.send_message(message.from_user.id, f'Все пользователи: {last_id}\nВсе запросы: {all_requests}\nСреднее кол-во запросов: {round(all_requests / last_id, 1)}', reply_markup=keyboards.statistic_button)


async def clear_requests(message: types.Message):
    await bot.send_message(message.from_user.id, 'успешно!')
    last_id = DB.get_last_id()
    for user_id in range(last_id):
        user_id += 1
        DB.clear_requests(user_id)


async def back_to_client_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=keyboards.kb_client)


async def command_admin(message: types.Message):
    result = DB.check_admin(message.from_user.id)
    if result is True:
        await bot.send_message(message.from_user.id, 'Админ панель', reply_markup=keyboards.kb_admin)


async def message_for_user(message: types.Message, state: FSMContext):
    await MSGforUser.chat_id.set()
    await bot.send_message(message.from_user.id, '<b>Введите Айди Чата</b>')


async def get_chat_id_for_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await MSGforUser.next()
    await bot.send_message(message.from_user.id, '<b>Введите сообщение!</b>')


async def send_message_for_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text

    async with state.proxy() as data:
        await bot.send_message(chat_id=data['chat_id'], text=f'♢<i><b> Сообщение от Администрации </b></i>♢\n\n{data["msg"]}')
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_admin, filters.Text(startswith='adm'))
    dp.register_message_handler(admin_mailing, filters.Text(startswith='Рассылка'))
    dp.register_message_handler(bot_statistic, filters.Text(startswith='Статистика бота'))
    dp.register_message_handler(message_for_user, filters.Text(startswith='Сообщение юзеру'), state=None)
    dp.register_message_handler(back_to_client_kb, filters.Text(startswith='Назад'))
    dp.register_message_handler(get_chat_id_for_msg, state=MSGforUser.chat_id)
    dp.register_message_handler(send_message_for_user, state=MSGforUser.msg)
    dp.register_callback_query_handler(clear_requests, lambda callback_query: callback_query.data == 'clear_requests')
    dp.register_message_handler(send_mailing, state=FSMAdmin.msg)