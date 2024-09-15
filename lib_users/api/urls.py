from django.urls import path
from lib_users.api.views.register import RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
]
