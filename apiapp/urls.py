from django.urls import path, include
from apiapp import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'orders', views.OrderListApiView, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
]