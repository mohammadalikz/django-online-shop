from django import forms
from django.forms import ModelForm
from .models import Coupon


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('code',)