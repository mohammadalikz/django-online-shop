from django.views.generic import ListView, DetailView

from cart.form import CartAddForm
from .models import *
from django.views.generic.edit import FormMixin

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


class ProductDetail(FormMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    form_class = CartAddForm

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(slug=slug)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)