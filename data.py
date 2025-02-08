class ApiCodeMessages:

    # Сообщения ответов на создание аккаунта
    success_message_account_created = '"ok":true'
    create_error_message_field_missed = "Недостаточно данных для создания учетной записи"
    create_error_message_login_used = "Этот логин уже используется"

    # Сообщения ответов на логин
    success_message_login = 'id'
    login_error_message_field_missed = 'Недостаточно данных для входа'
    login_error_message_wrong_login = 'Учетная запись не найдена'

    # Сообщения ответов на создание заказа
    success_message_order_created = 'track'

    # Сообщение ответа на получение списка заказов
    order_list_message = 'orders'

    # Сообщение ответа на удаление аккаунта
    success_message_account_deleted = '"ok":true'
    delete_error_wrong_id = 'Курьера с таким id нет'

def get_order_data(color):
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": [color]
    }