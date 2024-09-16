from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from books.models import Book, Copies, CopyStatus
from books.api.serializers.books import BookSerializer
from django.db.models import Count


class PublicBook:
     def get_books(self, request):
        page_number = request.query_params.get('page', 1)
        page_size = int(request.query_params.get('page_size', 3)) 
        
        books_queryset = Book.objects.all()
        paginator = Paginator(books_queryset, page_size)
        
        try:
            page_books = paginator.page(page_number)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookSerializer(page_books, many=True)

        
        response_data = {
            'count': paginator.count,
            'results': serializer.data,
            'next': page_books.next_page_number() if page_books.has_next() else None,
            'previous': page_books.previous_page_number() if page_books.has_previous() else None
        }

        return Response(response_data, status=status.HTTP_200_OK)




    