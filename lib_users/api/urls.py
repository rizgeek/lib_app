from django.urls import path
from lib_users.api.views.register import RegisterView
from lib_users.api.views.login import LoginView
from lib_users.api.views.user import UserLib

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user/<str:action>', UserLib.as_view(), name='user'),
]
