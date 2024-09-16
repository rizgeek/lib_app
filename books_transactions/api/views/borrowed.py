from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from books_transactions.api.controller.borrowed import BorrowBook


class Borrowed(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.borrowed = BorrowBook()

    def post(self, request, action):
        match action :
            case 'borrowed' :
                return self.borrowed.borrow_books(request)
            case _ :
                return Response({
                    'message' : 'action not found'
                }, status=status.HTTP_404_NOT_FOUND)




    
