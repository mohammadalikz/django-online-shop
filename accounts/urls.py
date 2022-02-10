from django.urls import path
from .views import Profile, Register, Login, home, Logout

app_name = 'accounts'
urlpatterns = [
    path('', home, name='home'),
    path('profile/', Profile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
