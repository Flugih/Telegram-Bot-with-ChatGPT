from aiogram import types, Dispatcher, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from createBot import bot
import os
import openai
import keyboards
import DB
import secrets
import payment
from datetime import timedelta, date

openai.api_key = os.getenv('OPENAI_API')


class FSMClient(StatesGroup):
    reason = State()


async def command_support(message: types.Message):
    await bot.send_message(message.from_user.id, text='Поддержка', reply_markup=keyboards.sup_button)


async def about_support(message: types.Message):
    # if message.text == 'Поддержка':
    await FSMClient.reason.set()
    await bot.send_message(message.from_user.id, 'Пожалуйста, опишите вашу проблему или предложите свою идею.')


async def send_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await bot.send_message(message.from_user.id, 'Ваша заявка успешно отправлена!')

    async with state.proxy() as data:
        await bot.send_message(chat_id=os.getenv('SUP_CHAT'), text=f'Новая заявка!\n\nПричина: \"{data["reason"]}\"\nОтправитель: {message.from_user.first_name}\nАйди чата: {message.from_user.id}', reply_markup=keyboards.sup_confirm_button)
    await state.finish()


async def delete_message_handler(callback_query):
    # Получаем id чата и id сообщения из callback_query
    msg_id = callback_query.message.message_id

    # Удаляем сообщение
    await bot.delete_message(chat_id=os.getenv('SUP_CHAT'), message_id=msg_id)

    # Отвечаем на callback_query, чтобы убрать уведомление "Жмите для дальнейших действий"
    await callback_query.answer()


async def message_handler(message: types.Message):
    day_of_purchase = DB.get_day_of_purchase(message.from_user.id)
    days = None
    if day_of_purchase is not None:
        days = date.today() - day_of_purchase

    if days is not None and days.days >= 30 :
        DB.end_of_sub(message.from_user.id)

    if 'Default' in DB.get_status(message.from_user.id):
        free_requests = DB.get_free_requests(message.from_user.id)
        if free_requests != 0:
            try:
                response = await openai.Completion.acreate(
                    engine="text-davinci-003",
                    prompt=message.text,
                    max_tokens=3000,
                    n=1,
                    stop=None,
                    top_p=1,
                    temperature=0.5,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                await message.answer(response.choices[0].text)
                DB.add_requests(message.from_user.id)
                await bot.send_message(message.from_user.id, f'<b>У вас осталось {free_requests - 1} запрос(-а)</b>', parse_mode="HTML")
                DB.change_free_requests(message.from_user.id, free_requests - 1)
            except Exception as ex:
                await bot.send_message(message.from_user.id, '<b>Повторите попытку!</b>', parse_mode="HTML")
                print('(ERROR)', ex)
        elif free_requests == 0:
            await bot.send_message(message.from_user.id, '<b>❌Ошибка!\nПодписку можно купить в разделе "Профиль"</b>', parse_mode="HTML")
    elif 'Admin' or 'Vip' in DB.get_status(message.from_user.id):
        # messages = message.text
        # messages.append({"role": "user", "content": message.text})
        try:
            response = await openai.Completion.acreate(
                engine="text-davinci-003",
                prompt=message.text,
                max_tokens=3000,
                n=1,
                stop=None,
                top_p=1,
                temperature=0.5,
                frequency_penalty=0,
                presence_penalty=0,
            )
            await message.answer(response.choices[0].text)
            DB.add_requests(message.from_user.id)
        except Exception as ex:
            await bot.send_message(message.from_user.id, '<b>Повторите попытку!</b>', parse_mode="HTML")
            print('(ERROR)', ex)


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код</b>', reply_markup=keyboards.kb_client, parse_mode="HTML")
    DB.add_chat_id(message.from_user.id)


async def information_about_bot(message: types.Message):
    await bot.send_message(message.from_user.id, '♦ <b>Что делает этот бот?</b>\n<i>Бот может ответить на любой ваш вопрос! Просто задай его.</i>\n\n♦ <b>Что дает подписка?</b>\n<i>Подписка дает доступ к безлимитному использованию бота на месяц.</i>', parse_mode="HTML")


async def user_profile(message: types.Message):
    day_of_purchase = DB.get_day_of_purchase(message.from_user.id)
    days = None
    if day_of_purchase is not None:
        days = date.today() - day_of_purchase

    if days is not None and days.days >= 30:
        DB.end_of_sub(message.from_user.id)

    if day_of_purchase is None:
        data = '  -  '
    else:
        data = day_of_purchase + timedelta(days=30)

    requests = DB.get_requests_client(message.from_user.id)
    status = DB.get_status(message.from_user.id)
    await bot.send_message(message.from_user.id, f'📊 <b>Ваш профиль:</b>\n\n👤<b>Имя</b>: {message.from_user.first_name}\n🔸<b>Ваши запросы:</b> {requests}\n\n💎<b>Статус</b>: {status}\n⌛<b>Закончится</b>: {data}', reply_markup=keyboards.buy_button, parse_mode="HTML")


async def buy_vip(message: types.Message):
    if 'Default' in DB.get_status(message.from_user.id):
        secret_key = secrets.token_urlsafe()
        pay_link = payment.create_paylink(secret_key)
        DB.write_payment_token(message.from_user.id, secret_key)
        await bot.send_message(message.from_user.id, '<b>Название:</b> VIP\n<b>Стоимость:</b> 149₽\n<b>Срок действия:</b> 30 дней', reply_markup=keyboards.create_pay_button(pay_link), parse_mode="HTML")
    else:
        await bot.send_message(message.from_user.id, 'Подписка уже активна!')


async def check_payment(message: types.Message):
    secret_key = DB.get_temp_payment_token(message.from_user.id)
    payment_status = payment.check_pay_status(secret_key)
    if payment_status is not None and 'success' in payment_status:
        await bot.send_message(message.from_user.id, '✅ Успешная оплата!')
        DB.success_pay(message.from_user.id, date.today())
        DB.write_payment_token(message.from_user.id, 0)
    else:
        await bot.send_message(message.from_user.id, '❌ Вы еще не оплатили!')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(information_about_bot, filters.Text(startswith='ℹ Помощь'))
    dp.register_message_handler(user_profile, filters.Text(startswith='👤 Профиль'))
    dp.register_message_handler(command_support, filters.Text(startswith='❗ Поддержка'))
    dp.register_callback_query_handler(about_support, lambda callback_query: callback_query.data == 'write_to_sup')
    dp.register_callback_query_handler(delete_message_handler, lambda callback_query: callback_query.data == 'remove')
    dp.register_callback_query_handler(check_payment, lambda callback_query: callback_query.data == 'check_payment')
    dp.register_callback_query_handler(buy_vip, lambda callback_query: callback_query.data == 'buy_vip')
    dp.register_message_handler(send_reason, state=FSMClient.reason)
    dp.register_message_handler(message_handler)