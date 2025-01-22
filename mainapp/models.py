import ast
from django.db import models
from django.urls import reverse


class Order(models.Model):
    class Meta:
        ordering = ('-id', )
        verbose_name = 'Order'

    table_number = models.IntegerField()
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
        total = 0
        items_ = ast.literal_eval(self.items)

        for item in items_:
            total += item['price'] * item.get('count', 1)  # учитываем количество
        self.total_price = total

    def get_absolute_url(self):
        return reverse('order_list')
