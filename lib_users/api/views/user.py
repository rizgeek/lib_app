from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from lib_users.api.controller.user import UserController

class UserLib(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.user = UserController()

    def get(self, request, action):
        match action :
            case 'profile' :
                return self.user.profile(request) 
            case _ : 
                return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)