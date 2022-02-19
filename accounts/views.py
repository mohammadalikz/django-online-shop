from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from .models import User
from .forms import SignupForm, ProfileForm
from django.shortcuts import redirect
from .mixins import LoginRedirectMixin
from django.contrib import messages


# Create your views here.
def home(request):
    return redirect('accounts:login')


class Login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = 'accounts:profile'
    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, 'you successfully login')
        return super().form_valid(form)



class Logout(LogoutView):
    template_name = 'accounts/login.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Register(LoginRedirectMixin, CreateView):
    form_class = SignupForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


