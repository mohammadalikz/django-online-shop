from django.urls import path
from .views import *

app_name = 'shop'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),

]
