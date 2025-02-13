import json
import allure
import pytest
import requests
from data import ApiCodeMessages, get_order_data
from urls import AppUrls


class TestOrderCreate:

    @allure.title('Создание заказа')
    @allure.description('Создаём заказ с разными параметрами цвета, сверяем код и сообщение ответа')
    @pytest.mark.parametrize('color', ['black', 'grey', '""'])
    def test_order_create_valid_data_returns_trackid(self, color):
        # данные заказа, цвет параметризирован
        order_data = get_order_data(color)

        # сериализируем запрос в json
        data_json = json.dumps(order_data)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(AppUrls.main_url + AppUrls.create_order_url, data=data_json, headers=headers)

        # сверяем код ответа
        assert response.status_code == 201

        # сверяем сообщение ответа
        assert ApiCodeMessages.success_message_order_created in response.text


class TestOrderGetList:

    @allure.title('Получение списка заказов по id курьера')
    @allure.description('Создаётся новый курьер, выводится список его заказов')
    def test_order_get_list_by_courier_id(self, create_login_delete_courier):

        # распаковываем ответ на логин из фикстуры
        _, login_response, __ = create_login_delete_courier

        # сохраняем id курьера
        courier_id = login_response.json()['id']

        payload = {'courierId': courier_id}

        repsonse = requests.get(AppUrls.main_url + AppUrls.get_courier_orders, params=payload)

        # сверяем код ответа
        assert repsonse.status_code == 200

        # сверяем сообщение ответа
        assert ApiCodeMessages.order_list_message in repsonse.text
