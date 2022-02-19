from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from shop.models import Product
from .cart import Cart
from .form import CartAddForm
from django.views.generic.edit import DeleteView
class Detail(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'])
        return redirect('cart:detail')

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:detail')