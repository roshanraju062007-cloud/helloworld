from django.urls import path
from .views import Home, login

urlpatterns = [
    path('Home', Home),
    path('login', login, name='login'),
]