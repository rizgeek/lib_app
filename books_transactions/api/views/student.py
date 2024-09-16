from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from books_transactions.api.controller.transaction_student import TransactionStudent


class StudentTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.student = TransactionStudent()

    def get(self, request, action) :
        match action :
            case 'histories' :
                return self.student.get_history(request)
            case _ :
                return Response({
                    'message' : 'action not found'
                }, status=status.HTTP_404_NOT_FOUND)







    