from django.urls import path
from .views import *

app_name = 'orders'
#
urlpatterns = [
    path('<int:pk>/', Detail.as_view(), name='detail'),
    path('create/', order_create, name='create'),
    path('payment/<int:order_id>/<price>/', payment, name='payment'),
    path('verify/', verify, name='verify'),
    path('apply/<int:order_id>/', coupon_apply, name='coupon_apply'),

]
