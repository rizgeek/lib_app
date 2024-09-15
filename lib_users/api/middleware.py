from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        jwt_auth = JWTAuthentication()

        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                prefix, token = auth_header.split(' ')
                if prefix.lower() != 'bearer':
                    raise AuthenticationFailed('Invalid token prefix.')
                
                user, _ = jwt_auth.get_user(validated_token=jwt_auth.get_validated_token(token))
                print(user)
                request.user = user
            except (AuthenticationFailed, ValueError) as e:
                request.user = None
        else:
            request.user = None

