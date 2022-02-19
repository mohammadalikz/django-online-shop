from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='email', help_text=None)

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2')



class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]
