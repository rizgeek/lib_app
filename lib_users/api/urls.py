from django.urls import path
from lib_users.api.views.register import RegisterView
from lib_users.api.views.login import LoginView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
]
