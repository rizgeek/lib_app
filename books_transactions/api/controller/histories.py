from rest_framework.response import Response
from rest_framework import status
from lib_users.permissions import IsInGroup
from books_transactions.models import Histories, FlagTransaction
from books_transactions.api.serializers.histories import HistoriesSerializer
from django.contrib.auth.models import User

class HistoriesBook:
    def get_history(self, request) :
        IsInGroup.check_access(request, self, 'librarian')

        email = request.GET.get('email-student')

        if not email :
            return Response({'message ': "this endpoint require email-student"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist :
            return Response({"message" : f"user with email {email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)


        objects_active = Histories.objects.filter(user=user, status=FlagTransaction.active)
        serializers_active = HistoriesSerializer(objects_active, many=True)
        
        objects_returned = Histories.objects.filter(user=user, status=FlagTransaction.returned)
        serializers_return = HistoriesSerializer(objects_returned, many=True)

        data = {
            'active': serializers_active.data,
            'returned': serializers_return.data
        }

        return Response(data, status=status.HTTP_200_OK)
