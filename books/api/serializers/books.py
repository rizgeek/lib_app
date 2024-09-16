from rest_framework import serializers
from books.models import Book, Copies, CopyStatus
from books_transactions.models import Histories, FlagTransaction
from django.utils.timezone import now

class BookSerializer(serializers.ModelSerializer):
    copies = serializers.SerializerMethodField()
    copies_ids = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    borrowable_status = serializers.SerializerMethodField()
    

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'edition', 'status', 'copies','copies_ids' ,'borrowable_status']

    def get_copies(self, obj):
        return Copies.objects.filter(book=obj, status=CopyStatus.AVAILABLE).count()

    def get_copies_ids(self, obj):
        # Fetch IDs of all copies for the book
        return Copies.objects.filter(book=obj, status=CopyStatus.AVAILABLE).values_list('id', flat=True)
    
    def get_status(self, obj):
        copies_count = self.get_copies(obj)
        return CopyStatus.NOT_AVAILABLE if copies_count < 1 else CopyStatus.AVAILABLE
    
    def get_borrowable_status(self, obj):
        copies_count = self.get_copies(obj)

        if copies_count > 0:
            return 'Now'
        
        active_histories = Histories.objects.filter(
            book_copies__book=obj, 
            status=FlagTransaction.active,
            end_date__gte=now()
        ).order_by('end_date')

        if active_histories.exists():
            closest_end_date = active_histories.first().end_date
            return f'Next available on {closest_end_date.strftime("%Y-%m-%d")}'
        
        return 'Out off stock'



class CopiesSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    
    book_details = BookSerializer(source='book', read_only=True)

    class Meta:
        model = Copies
        fields = ['id', 'book', 'status', 'book_details']
