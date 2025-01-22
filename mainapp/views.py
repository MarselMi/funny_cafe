import ast
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from mainapp.forms import CreateOrderForm, UpdateOrder
from mainapp.models import Order
from django.db.models import Sum


class CreateOrder(CreateView):
    model = Order
    form_class = CreateOrderForm
    template_name = 'mainapp/order_create_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.calculate_total_price()
        instance.save()
        return redirect('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Создание заказа'
        return context


class OrderList(TemplateView):
    template_name = 'mainapp/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.all()
        context["title"] = 'Список заказов'
        return context


class UpdateOrderView(UpdateView):
    model = Order
    form_class = UpdateOrder
    template_name = 'mainapp/order_update_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.calculate_total_price()
        instance.save()
        return redirect('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Изменение заказа'
        return context


class DeleteOrderView(DeleteView):
    model = Order
    success_url = '/'


class RevenueView(TemplateView):
    template_name = 'mainapp/sum_order_price.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прибыль за смену'
        context['total_revenue'] = Order.objects.filter(status='paid').aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0
        return context


class SearchOrders(TemplateView):

    def get(self, request, *args, **kwargs):
        param = request.GET.get('q').strip()
        status_dict = {
            'в ожидании': 'pending',
            'готово': 'ready',
            'оплачено': 'paid'
        }

        if status_dict.get(param.lower()):
            param = status_dict.get(param.lower())
        orders = Order.objects.filter(table_number__icontains=param) | Order.objects.filter(status__icontains=param)
        return render(request, 'mainapp/order_list.html', {'orders': orders})
