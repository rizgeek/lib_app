from django.urls import path
from books_transactions.api.views.transactions import BooksTransaction

urlpatterns = [
    path('transaction/<str:action>', BooksTransaction.as_view(), name='Books Transactions'),
]
