import json
from rest_framework import status
from rest_framework.test import APITestCase
from mainapp.models import Order


class OrderApiTest(APITestCase):
    url = '/api-v1/orders/'

    def test_create_order(self):
        '''Проверяет создание заказа с валидными данными.'''
        data = {
            'table_number': 1,
            'items': '[{"name": "Pizza", "price": 10.00}, {"name": "Soda", "price": 2.50}]'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.total_price, 12.50)
        self.assertIn('Pizza', order.items)
        self.assertIn('Soda', order.items)

    def test_create_order_with_count(self):
        '''Проверяет создание заказа с указанием количества товаров.'''
        data = {
            'table_number': 2,
            'items': '[{"name": "Burger", "price": 8.00, "count": 2}, {"name": "Fries", "price": 3.00}]'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_price, 19.00)

    def test_create_order_invalid_data(self):
        '''Проверяет обработку невалидных JSON данных.'''
        data = {
            'table_number': 3,
            'items': 'invalid json'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_missing_fields(self):
        '''Проверяет обработку запроса с отсутствующими обязательными полями.'''
        data = {
            'table_number': 4,
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_list_orders(self):
        '''Проверяет получение списка заказов.'''
        Order.objects.create(table_number=1, items='[{"name": "Pizza", "price": 10}]', total_price=10)
        Order.objects.create(table_number=2, items='[{"name": "Burger", "price": 5}]', total_price=5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), 2)

    def test_filter_orders_by_table_number(self):
        '''Проверяет фильтрацию заказов по номеру стола.'''
        Order.objects.create(table_number=1, items='[{"name": "Pizza", "price": 10}]', total_price=10)
        Order.objects.create(table_number=21, items='[{"name": "Burger", "price": 5}]', total_price=5)
        url = '/api-v1/orders/?table_number=21'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), 1)
        self.assertEqual(response.json().get('results')[0]['table_number'], 21)

    def test_filter_orders_by_status(self):
        '''Проверяет фильтрацию заказов по статусу.'''
        Order.objects.create(table_number=1, items='[{"name": "Pizza", "price": 10}]', total_price=10, status='pending')
        Order.objects.create(table_number=2, items='[{"name": "Burger", "price": 5}]', total_price=5, status='paid')
        url = '/api-v1/orders/?status=paid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), 1)
        self.assertEqual(response.json().get('results')[0]['status'], 'paid')
