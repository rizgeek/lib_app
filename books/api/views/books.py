from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from books.api.controller.books import Books
from books.api.controller.public_books import PublicBook

class Library(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.books = Books()

    def post(self, request, action) :
        match action :
            case 'books' :
                return self.books.create_books(request)
            case _ :
                return Response({
                    'message' : 'action not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
class PublicLib(APIView):
    def __init__(self) -> None:
        self.books = PublicBook()

    def get(self, request, action):
        match action :
            case 'books':
                return self.books.get_books(request)