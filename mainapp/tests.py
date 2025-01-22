import ast
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from mainapp.models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.order1 = Order.objects.create(
            table_number=1,
            items='[{"name": "Pizza", "price": 10.00}, {"name": "Soda", "price": 2.50}]',
        )
        self.order2 = Order.objects.create(
            table_number=2,
            items='[{"name": "Burger", "price": 8.00, "count": 2}, {"name": "Fries", "price": 3.00}]',
        )
        self.order3 = Order.objects.create(
            table_number=3,
            items='[{"name": "Salad", "price": 6.50}, {"name": "Water", "price": 1.00, "count": 3}]',
            status='paid'
        )

    def test_order_creation(self):
        '''Проверяет правильность создания объектов Order и начальные значения полей.'''
        self.assertEqual(Order.objects.count(), 3)
        self.assertEqual(self.order1.table_number, 1)
        self.assertEqual(self.order2.status, 'pending')
        self.assertEqual(self.order3.status, 'paid')

    def test_default_status(self):
        ''' Проверяет значение статуса по умолчанию.'''
        order = Order.objects.create(table_number=4, items='[]')
        self.assertEqual(order.status, 'pending')

    def test_calculate_total_price(self):
        '''Проверяет корректность расчета total_price'''
        self.order1.calculate_total_price()
        self.assertEqual(self.order1.total_price, Decimal('12.50'))

        self.order2.calculate_total_price()
        self.assertEqual(self.order2.total_price, Decimal('19.00'))

        self.order3.calculate_total_price()
        self.assertEqual(self.order3.total_price, Decimal('9.50'))

    def test_calculate_total_price_with_no_items(self):
        '''Проверяет, что если в заказе нет позиций, цена будет 0.'''
        order = Order.objects.create(table_number=5, items='[]')
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('0'))

    def test_calculate_total_price_with_missing_count(self):
        ''' Проверяет, что если не указано количество, то берется 1.'''
        order = Order.objects.create(table_number=6, items='[{"name": "Ice Cream", "price": 5.00}]')
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('5.00'))

    def test_items_parsing(self):
        '''Проверяет правильность преобразования строки items в Python-список.'''
        items = ast.literal_eval(self.order1.items)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Pizza')
        self.assertEqual(items[1]['price'], 2.50)

        items = ast.literal_eval(self.order2.items)
        self.assertEqual(items[0]['count'], 2)

    def test_get_absolute_url(self):
        '''Проверяет возврат правильного URL-адреса.'''
        self.assertEqual(self.order1.get_absolute_url(), reverse('order_list'))

    def test_ordering(self):
        '''Проверяет порядок записей по умолчанию.'''
        orders = Order.objects.all()
        self.assertEqual(list(orders), [self.order3, self.order2, self.order1])

    def test_verbose_name(self):
        '''Проверяет verbose name модели.'''
        self.assertEqual(str(Order._meta.verbose_name), 'Order')