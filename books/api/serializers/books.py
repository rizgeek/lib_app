from rest_framework import serializers
from books.models import Book, Copies, CopyStatus

class BookSerializer(serializers.ModelSerializer):
    copies = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    borrowable_status = serializers.SerializerMethodField()
    

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'edition', 'status', 'copies', 'borrowable_status']

    def get_copies(self, obj):
        return Copies.objects.filter(book=obj, status=CopyStatus.AVAILABLE).count()
    
    def get_status(self, obj):
        copies_count = self.get_copies(obj)
        return CopyStatus.NOT_AVAILABLE if copies_count < 1 else CopyStatus.AVAILABLE
    
    def get_borrowable_status(self, obj):
        copies_count = self.get_copies(obj)
        return 'Now' if copies_count > 1 else 'Not Now'


class CopiesSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Copies
        fields = ['book', 'status']
