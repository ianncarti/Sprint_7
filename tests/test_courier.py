import allure
import pytest
import requests
import helpers
from data import ApiCodeMessages
from urls import AppUrls


class TestCourierCreate:

    @allure.title('Регистрация аккаунта курьера')
    @allure.description('Регистрируем аккаунт и сверяем текст ответа')
    def test_courier_create_with_valid_creds_success(self, create_login_delete_courier):
        # распаковываем ответы из фикстуры
        reg_response, _, __ = create_login_delete_courier

        # проверяем код ответа
        assert reg_response.status_code == 201

        # проверяем сообщение ответа
        assert ApiCodeMessages.success_message_account_created in reg_response.text

    @allure.title('Регистрация аккаунта c занятым логином')
    @allure.description('Дважды отправляется запрос на регистрацию с одинаковыми данными')
    def test_courier_create_with_existing_login_error(self, create_login_delete_courier):
        # распаковываем ответы и креды из фикстуры
        reg_response, _, valid_creds = create_login_delete_courier

        # отправляем повторный запрос на регистрацию и сохраняем ответ в переменную
        response_with_error = requests.post(AppUrls.main_url + AppUrls.create_courier, data=valid_creds)

        # проверяем код ответа
        assert response_with_error.status_code == 409

        # проверяем сообщение ответа
        assert ApiCodeMessages.create_error_message_login_used in response_with_error.text

    @allure.title('Запрос на регистрацию аккаунта с неполными данными')
    @allure.description('В тесте с помощью параметризации отправляется запрос сперва без логина, затем без пароля')
    @pytest.mark.parametrize('cred', {'login', 'password'})
    def test_courier_create_missing_data_error(self, cred):
        # генерируем креды
        valid_creds = helpers.generate_uniq_creds()

        # удаляем логин/пароль из словаря с помощью параметризации
        valid_creds.pop(cred)

        # отправляем запрос на регистрацию без логина/пароля
        response_with_error = requests.post(AppUrls.main_url + AppUrls.create_courier, data=valid_creds)

        # проверяем код ответа
        assert response_with_error.status_code == 400

        # проверяем сообщение ответа
        assert ApiCodeMessages.create_error_message_field_missed in response_with_error.text


class TestCourierLogin:

    @allure.title('Логин курьера с валидными данными')
    @allure.description('Создание аккаунта и логин производятся в фикстуре, '
                        'в тесте сверяется код ответа и текст при успешном логине')
    def test_courier_login_valid_creds_success(self, create_login_delete_courier):
        # распаковываем ответ на логин из фикстуры
        _, login_response, __ = create_login_delete_courier

        # сверяем код ответа
        assert login_response.status_code == 200

        # сверяем сообщение ответа
        assert ApiCodeMessages.success_message_login in login_response.text

    @allure.title('Логин курьера с неполными данными')
    @allure.description('В логин и пароль по очереди передаётся пустая строка')
    @pytest.mark.parametrize('cred', ['login', 'password'])
    def test_courier_login_missing_data_error(self, create_login_delete_courier, cred):
        # распаковываем сгенерированные креды из фикстуры
        _, __, valid_creds = create_login_delete_courier

        # заменяем логин/пароль на пустую строку
        valid_creds[cred] = ''

        # делаем запрос с неполными данными
        login_response_error = requests.post(AppUrls.main_url + AppUrls.login_courier_url, data=valid_creds)

        # сверяем код ответа
        assert login_response_error.status_code == 400

        # сверяем сообщение ответа
        assert ApiCodeMessages.login_error_message_field_missed in login_response_error.text

    @allure.title('Логин курьера в несуществуюший аккаунт')
    @allure.description('В фикстуре создаётся новый аккаунт, затем его логин/пароль изменяются на несуществующие'
                        ' и отпарвляется запрос')
    @pytest.mark.parametrize('cred', ['login', 'password'])
    def test_courier_login_wrong_login_error(self, create_login_delete_courier, cred):
        #распаковываем сгенерированные креды из фикстуры
        _, __, valid_creds = create_login_delete_courier

        #изменяем логин/пароль курьера на невалидные добавлением '1'
        valid_creds[cred] = valid_creds[cred] + '1'

        # отправляем запрос на логин с невалидным логином/паролем
        login_response_error = requests.post(AppUrls.main_url + AppUrls.login_courier_url, data=valid_creds)

        # сверяем код ответа
        assert login_response_error.status_code == 404

        # сверяем сообщение ответа
        assert ApiCodeMessages.login_error_message_wrong_login in login_response_error.text

class TestCourierDelete:

    @allure.title('Удаление аккаунта курьера')
    @allure.description('В фикстуре производится создание и логин для получения id курьера, затем id передается в запрос'
                        'на удаление. Сверяется код и сообщение ответа')
    def test_courier_delete_by_id_success(self, create_login_delete_courier):
        # распаковываем ответ на логин из фикстуры
        _, login_response, __, = create_login_delete_courier

        # получаем id курьера
        courier_id = login_response.json()['id']

        # формируем body запроса на удаление, подставляем полученный id
        data_for_delete_request = {'id': courier_id}

        # форматируем url удаления, подставляем id курьера в url
        delete_url = AppUrls.delete_courier_url.format(id=courier_id)

        delete_response = requests.delete(AppUrls.main_url + delete_url, data=data_for_delete_request)

        # сверяем код ответа
        assert delete_response.status_code == 200

        # сверяем сообщение ответа
        assert ApiCodeMessages.success_message_account_deleted in delete_response.text

    @allure.title('Удаление аккаунта курьера с несуществущим id')
    @allure.description('В фикстуре производится создание и логин для получения id курьера, затем id изменяется'
                        'на несуществущий и отправляется запрос на удаление. Сверяется код и сообщение ответа')
    def test_courier_delete_wrong_id(self, create_login_delete_courier):
       # распаковываем ответ на логин из фикстуры
        _, login_response, __, = create_login_delete_courier

        # получаем id курьера и меняем его на несуществующий
        courier_id = login_response.json()['id'] + 1111111

        # формируем body запроса на удаление, подставляем полученный id
        data_for_delete_request = {'id': courier_id}

        # форматируем url удаления, подставляем id курьера в url
        delete_url = AppUrls.delete_courier_url.format(id=courier_id)

        delete_response = requests.delete(AppUrls.main_url + delete_url, data=data_for_delete_request)

        # сверяем код ответа
        assert delete_response.status_code == 404

        # сверяем сообщение ответа
        assert ApiCodeMessages.delete_error_wrong_id in delete_response.text