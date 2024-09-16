from lib_users.permissions import IsInGroup
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from lib_users.api.serializers.user import UserSerializer
from rest_framework.response import Response
from rest_framework import status



class UserController :

    permission_classes = [IsAuthenticated]

    def profile(self, request):
        IsInGroup.check_access(request, self, 'librarian', 'student')
                
        email = request.user
        try:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)