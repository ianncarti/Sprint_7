import pytest
import requests
import helpers
from urls import AppUrls


#Фикстура создаёт аккаунт курьера, делает логин, после теста удаляет аккаунт
@pytest.fixture
def create_login_delete_courier():
    #генерируем креды
    valid_creds = helpers.generate_uniq_creds()

    #отправляем запрос на регистрацию
    reg_response = requests.post(AppUrls.main_url + AppUrls.create_courier, data=valid_creds)

    #отправляем запрос на логин
    login_response = requests.post(AppUrls.main_url + AppUrls.login_courier_url, data=valid_creds)

    #сохраняем id из ответа на логин
    courier_id = login_response.json()['id']

    #формируем body запроса на удаление, подставляем полученный id
    data_for_delete_request = {'id': courier_id}

    #ждём пока выполнится код теста до удаления
    yield reg_response, login_response, valid_creds

    #форматируем url удаления, подставляем id курьера в url
    delete_url = AppUrls.delete_courier_url.format(id=courier_id)

    #отправляем запрос на удаление аккаунта
    requests.delete(AppUrls.main_url + delete_url, data=data_for_delete_request)

    #возвращаем кортеж из трёх ответов, а также креды от аккаунта
    return reg_response, login_response, valid_creds
