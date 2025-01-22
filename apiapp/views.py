import ast
from typing import Any

from rest_framework import viewsets, status
from rest_framework.response import Response
from apiapp.serializers import OrderSerializer
from mainapp.models import Order
from django_filters.rest_framework import DjangoFilterBackend


class OrderListApiView(viewsets.ModelViewSet):
    queryset: Any = Order.objects.all()
    serializer_class: Any = OrderSerializer

    filter_backends: Any = [DjangoFilterBackend]
    filterset_fields: list[str] = ['table_number', 'status', ]

    def create(self, request, *args, **kwargs):
        '''
        :param request:
        :param args:
        :param kwargs:
        :return:
        Create a model instance.
        '''
        table_number: str = self.request.data.get('table_number')
        items: str = self.request.data.get('items').strip()
        total: int = 0
        items_: list[dict[str:str] | dict[str:int]] = ast.literal_eval(items)
        for item in items_:
            total += item['price'] * item.get('count', 1)  # учитываем количество
        serializer: Any = self.get_serializer(data={'items': items, 'table_number': table_number, 'total_price': total})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers: dict[str:str] | dict = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
