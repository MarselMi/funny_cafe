from django.utils.translation import gettext_lazy as _
from django import forms
from mainapp.models import Order


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table_number', 'items',]
        labels = {
            'table_number': 'Номер стола',
            'items': 'Список заказа',
        }
        help_texts = {
            'items': _("в формате списка словарей [{'name': 'блюдо1', 'price': 100, 'count': 2}, ...]\n"
                     "'count' - количество заказов, необязательный аргумент, по дефолту count = 1"),
        }
        widgets = {
            "items": forms.Textarea(attrs={'cols': 30, "rows": 5},)
        }


class UpdateOrder(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status', 'items',]
        labels = {
            'status': 'Статус заказа',
            'items': 'Список заказа',
        }
        help_texts = {
            'items': _("в формате списка словарей [{'name': 'блюдо1', 'price': 100, 'count': 2}, ...]\n"
                     "'count' - количество заказов, необязательный аргумент, по дефолту count = 1"),
        }
        widgets = {
            "items": forms.Textarea(attrs={'cols': 30, "rows": 5},)
        }
