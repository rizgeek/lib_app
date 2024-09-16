from django.urls import path
from books_transactions.api.views.transactions import BooksTransaction
from books_transactions.api.views.student import StudentTransaction

urlpatterns = [
    path('transaction/<str:action>', BooksTransaction.as_view(), name='Books Transactions'),
    path('student/<str:action>', StudentTransaction.as_view(), name='Student Transactions'),
]
