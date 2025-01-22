from django.urls import path, include
from apiapp import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'orders', views.OrderListApiView, basename='orders')
# router.register(r'users', views.UserModelView, basename='users')
# router.register(r'bal-holders', views.BalanceHolderModelView, basename='bal_holders')
# router.register(r'pays-type', views.PayTypeModelView, basename='pays_type')
# router.register(r'sub-pay-type', views.SubPayTypeApiView, basename='sub_pay_type')


urlpatterns = [
    path('', include(router.urls)),
]