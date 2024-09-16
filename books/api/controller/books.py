from lib_users.permissions import IsInGroup
from rest_framework.permissions import IsAuthenticated
from books.api.serializers.books import BookSerializer, CopiesSerializer
from books.models import CopyStatus
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class Books:
    permission_classes = [IsAuthenticated]

    def create_books(self, request):
        IsInGroup.check_access(request, self, 'librarian')

        try:
            with transaction.atomic():
                serializer_book = BookSerializer(data=request.data)
                copies = request.data.get('copies')
                book = None

                if not copies or not str(copies).isdigit() or int(copies) <= 0:
                    copies = 1
                else:
                    copies = int(copies)
                
                if serializer_book.is_valid():
                    book = serializer_book.save()
                    
                    for _ in range(copies):
                        copies_data = {'book': book, 'status': CopyStatus.AVAILABLE}
                        serializer_copies = CopiesSerializer(data=copies_data)
                        
                        if serializer_copies.is_valid():
                            serializer_copies.save()
                        else:
                            return Response(serializer_copies.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                    return Response({
                        'message': f'Book created with {copies} copies.'
                    }, status=status.HTTP_201_CREATED)
                
                else:
                    return Response(serializer_book.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': f'Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)