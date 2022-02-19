from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('detail/', Detail.as_view(), name='detail'),
    path('add/<int:product_id>', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>', cart_remove, name='cart_remove'),
]
