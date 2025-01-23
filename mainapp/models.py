import ast
from django.db import models
from django.urls import reverse


class Order(models.Model):
    '''Класс модели Order для реализации хранения данных в БД'''
    class Meta:
        ordering = ('-id', )
        verbose_name = 'Order'

    table_number = models.PositiveSmallIntegerField()
    items = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('ready', 'Готово'),
            ('paid', 'Оплачено'),
        ],
        default='pending'
    )

    def calculate_total_price(self):
        '''Функция для подсчета стоимости заказа с учетом количества блюд'''
        total = 0
        items_: list[dict] = ast.literal_eval(self.items)  # преобразую данные со строкового типа в список словарей 

        for item in items_:
            total += item['price'] * item.get('count', 1)  # учитываем количество
        self.total_price = total

    def get_absolute_url(self):
        '''Переопределяю метод редиректа после успешного создания модели'''
        return reverse('order_list')
