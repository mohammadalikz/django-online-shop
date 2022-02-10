from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.


class Home(ListView):
    template_name = 'shop/home.html'
    context_object_name = 'products'
    model = Product


class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'shop/category_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Category.objects.filter(slug=slug)


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(slug=slug)
