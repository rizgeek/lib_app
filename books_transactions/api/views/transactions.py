from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from books_transactions.api.controller.borrowed import BorrowBook
from books_transactions.api.controller.returned import ReturnedBook



class BooksTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.borrowed = BorrowBook()
        self.returned = ReturnedBook()


    def post(self, request, action):
        match action :
            case 'borrowed' :
                return self.borrowed.borrow_books(request)
            case 'returned' :
                return self.returned.returned_books(request)
            case _ :
                return Response({
                    'message' : 'action not found'
                }, status=status.HTTP_404_NOT_FOUND)




    
