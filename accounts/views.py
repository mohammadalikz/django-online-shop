from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from .models import User
from .forms import SignupForm, ProfileForm
from django.shortcuts import redirect
from .mixins import LoginRedirectMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse


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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'registering'
        message = render_to_string('accounts/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('link has sent to your email. <a href="accounts/login">login</a>')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.save()
        return HttpResponse(' <a href="accounts/login">login</a> ')
    else:
        return HttpResponse(' <a href="accounts/register">try again</a>')
