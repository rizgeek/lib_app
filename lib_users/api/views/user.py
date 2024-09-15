from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from lib_users.permissions import IsInGroup
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from lib_users.api.serializers.user import UserSerializer

class UserLib(APIView):
    permission_classes = [IsAuthenticated]

    def _check_access(self, request, *access) -> None:
        check = IsInGroup(*access).has_permission(request, self)
        if not check :
            raise PermissionDenied("You do not have permission to access this resource.")

    def get(self, request, action):
        match action :
            case 'profile' :
                self._check_access(request, 'librarian', 'student')
                
                email = request.user
                try:
                    user = User.objects.get(email=email)
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                except User.DoesNotExist:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
            case _ : 
                return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)