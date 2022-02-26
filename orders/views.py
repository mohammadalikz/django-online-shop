from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Coupon
from cart.cart import Cart
from django.http import HttpResponse
from django.contrib import messages
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from suds.client import Client
from django.views import View


class Detail(LoginRequiredMixin, CreateView):
    form_class = CouponForm
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['order'] = Order.objects.get(id=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Order.objects.get(pk=pk)


@login_required
def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
    cart.clear()
    return redirect('orders:detail', order.id)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "پرداخت مونگارد"
mobile = '09123456789'
CallbackURL = 'http://localhost:8000/orders/verify/'


@login_required
def payment(request, order_id, price):
    global amount, o_id
    amount = price
    o_id = order_id
    user = request.user
    order_id = user.
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order = Order.objects.get(id=o_id)
            order.paid = True
            order.save()
            messages.success(request, 'Transaction was successful', 'success')
            return redirect('shop:home')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted')
        else:
            return HttpResponse('Transaction failed.')
    else:
        return HttpResponse('Transaction failed or canceled by user')


@require_POST
def coupon_apply(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)

            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:detail', order_id)
        except Coupon.DoesNotExist:
            messages.error(request, 'This coupon does not exist', 'danger')
            return redirect('orders:detail', order_id)



