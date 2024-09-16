from rest_framework import serializers
from books.models import Book, Copies, CopyStatus
from books_transactions.models import Histories

class BorrowedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Copies
        fields = ['book_copies', 'user', 'status', 'start_date', 'end_date']
