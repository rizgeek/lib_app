from django.urls import path
from books_transactions.api.views.borrowed import Borrowed

urlpatterns = [
    path('transaction/<str:action>', Borrowed.as_view(), name='Transaction Borrowed'),
]
