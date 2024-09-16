from rest_framework.response import Response
from rest_framework import status
from lib_users.permissions import IsInGroup
from books_transactions.models import Histories, FlagTransaction
from books_transactions.api.serializers.histories import HistoriesSerializer

class TransactionStudent:
    def get_history(self, request) :
        IsInGroup.check_access(request, self, 'student')

        email = request.user
        objects_active = Histories.objects.filter(user=email, status=FlagTransaction.active)
        serializers_active = HistoriesSerializer(objects_active, many=True)
        
        objects_returned = Histories.objects.filter(user=email, status=FlagTransaction.returned)
        serializers_return = HistoriesSerializer(objects_returned, many=True)

        data = {
            'active': serializers_active.data,
            'returned': serializers_return.data
        }

        return Response(data, status=status.HTTP_200_OK)
