from typing import Any

from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from mainapp.forms import CreateOrderForm, UpdateOrder
from mainapp.models import Order
from django.db.models import Sum


class CreateOrder(CreateView):
    """
    View for creating a new object, with a response rendered by a template.
    """
    model: Order = Order
    form_class: CreateOrderForm = CreateOrderForm
    template_name: str = 'mainapp/order_create_form.html'

    def form_valid(self, form):
        '''
        :param form:
        :return:
        Если запрос валиден, перед сохранением производится подсчет суммы заказа
        '''
        instance: Any = form.save(commit=False)  # commit=False, обьект создается но не сохраняется для выполнения дальнейших действий
        instance.calculate_total_price()  # подсчет итоговой цены заказа 
        instance.save()  # сохранение созданного обьекта
        return redirect('order_list')

    def get_context_data(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context["title"] = 'Создание заказа'
        return context


class OrderList(TemplateView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    Страница со списком заказов
    """
    template_name: str = 'mainapp/order_list.html'

    def get_context_data(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.all()
        context["title"] = 'Список заказов'
        return context


class UpdateOrderView(UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    Страница обноления данных заказа
    """
    model: Order = Order
    form_class: UpdateOrder = UpdateOrder
    template_name: str = 'mainapp/order_update_form.html'

    def form_valid(self, form):
        '''
        :param form:
        :return:
        Если запрос валиден, перед сохранением производится подсчет суммы заказа
        '''
        instance = form.save(commit=False)
        instance.calculate_total_price()
        instance.save()
        return redirect('order_list')

    def get_context_data(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context["title"] = 'Изменение заказа'
        return context


class DeleteOrderView(DeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    model: Order = Order
    success_url: str = '/'


class RevenueView(TemplateView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    Страница с подсчетом суммарного заработка
    """
    template_name: str = 'mainapp/sum_order_price.html'

    def get_context_data(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прибыль за смену'
        context['total_revenue'] = Order.objects.filter(status='paid').aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0
        return context


class SearchOrders(TemplateView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    Представление для поиска заказов
    """
    def get(self, request, *args, **kwargs):
        '''
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        param = request.GET.get('q').strip()
        status_dict: dict[str:str] = {
            'в ожидании': 'pending',
            'готово': 'ready',
            'оплачено': 'paid'
        }
        if status_dict.get(param.lower()):
            param: str = status_dict.get(param.lower())
        orders: Order = Order.objects.filter(table_number__icontains=param) | Order.objects.filter(status__icontains=param)
        return render(request, 'mainapp/order_list.html', {'orders': orders})
