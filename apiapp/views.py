import ast
from rest_framework import viewsets, status
from rest_framework.response import Response
from apiapp.serializers import OrderSerializer
from mainapp.models import Order
from django_filters.rest_framework import DjangoFilterBackend


class OrderListApiView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table_number', 'status', ]

    def create(self, request, *args, **kwargs):
        table_number = self.request.data.get('table_number')
        items = self.request.data.get('items')
        total = 0
        items_ = ast.literal_eval(items)
        for item in items_:
            total += item['price'] * item.get('count', 1)  # учитываем количество
        serializer = self.get_serializer(data={'items': items, 'table_number': table_number, 'total_price': total})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
