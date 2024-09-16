from rest_framework import serializers
from books_transactions.models import Histories

class HistoriesSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(source='book_copies.book.isbn', read_only=True)
    title = serializers.CharField(source='book_copies.book.title', read_only=True)
    author = serializers.CharField(source='book_copies.book.author', read_only=True)
    publisher = serializers.CharField(source='book_copies.book.publisher', read_only=True)
    edition = serializers.CharField(source='book_copies.book.edition', read_only=True)
    copies = serializers.IntegerField(source='book_copies.book.copies', read_only=True)  # Assuming a 'copies' field in Book

    class Meta:
        model = Histories
        fields = ['status', 'isbn', 'title', 'author', 'publisher', 'edition', 'copies', 'status', 'user', 'start_date', 'end_date', 'action_date']
