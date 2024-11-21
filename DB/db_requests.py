from .db_connect import connection


def add_chat_id(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT id FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        rows = cursor.fetchall()
        if not rows:
            cursor.execute(
                f"""INSERT INTO "TGdatabase"."ChatGPT" (user_status, telegram_chat_id, requests, free_requests) VALUES ('Default', {chat_id}, 0, 3)"""
            )
        connection.commit()


def check_admin(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT user_status FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        if 'Admin' in cursor.fetchone()[0]:
            return True
        connection.commit()


def average_requests(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT requests FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )


def add_requests(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT requests FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        all_requests = cursor.fetchone()[0]
        all_requests += 1
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET requests = {all_requests} WHERE telegram_chat_id = {chat_id}"""
        )
        connection.commit()
        # return cursor.fetchone()[0]


def get_last_id():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT id FROM "TGdatabase"."ChatGPT" ORDER BY ID DESC LIMIT 1"""
        )
        return cursor.fetchone()[0]


def get_chat_id(id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT telegram_chat_id FROM "TGdatabase"."ChatGPT" WHERE id = {id}"""
        )
        return cursor.fetchone()[0]


def get_requests(id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT requests FROM "TGdatabase"."ChatGPT" WHERE id = {id}"""
        )
        return cursor.fetchone()[0]


def get_requests_client(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT requests FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        return cursor.fetchone()[0]


def get_status(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT user_status FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        return cursor.fetchone()[0]


def clear_requests(id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET requests = 0 WHERE id = {id}"""
        )
        connection.commit()


def success_pay(chat_id, date):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET user_status = 'Vip' WHERE telegram_chat_id = {chat_id}"""
        )
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET day_of_purchase = '{date}' WHERE telegram_chat_id = {chat_id}"""
        )
        connection.commit()


def end_of_sub(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET user_status = 'Default' WHERE telegram_chat_id = {chat_id}"""
        )
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET day_of_purchase = null WHERE telegram_chat_id = {chat_id}"""
        )
        connection.commit()


def get_day_of_purchase(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT day_of_purchase FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        return cursor.fetchone()[0]


def write_payment_token(chat_id, token):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET temp_payment_token = '{token}' WHERE telegram_chat_id = {chat_id}"""
        )
        connection.commit()


def get_temp_payment_token(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT temp_payment_token FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        return cursor.fetchone()[0]


def get_free_requests(chat_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT free_requests FROM "TGdatabase"."ChatGPT" WHERE telegram_chat_id = {chat_id}"""
        )
        return cursor.fetchone()[0]


def change_free_requests(chat_id, requests):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE "TGdatabase"."ChatGPT" SET free_requests = {requests} WHERE telegram_chat_id = {chat_id}"""
        )
        connection.commit()