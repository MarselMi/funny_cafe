from django.urls import path
from mainapp import views


urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('add/', views.CreateOrder.as_view(), name='add_order'),
    path('update/<int:pk>/', views.UpdateOrderView.as_view(), name='update_order'),
    path('delete/<int:pk>/', views.DeleteOrderView.as_view(), name='delete_order'),
    path('revenue/', views.RevenueView.as_view(), name='revenue'),
    path('search/', views.SearchOrders.as_view(), name='search_orders'),
]
