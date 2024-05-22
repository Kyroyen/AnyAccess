from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from utils.get_reqtotoken import request_to_auth_token
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode

from django.contrib.auth.models import User


# Create your views here.

class CustomAuth(BaseTokenAuthentication):

    decode_algo = ["HS256"]

    def authenticate(self, request):
        
        auth_type, secret_token = request_to_auth_token(request)

        try:
            # print(secret_token)
            ua = decode(secret_token, "secret", algorithms= self.decode_algo)
            # print(ua)
        except UnicodeError:
            raise AuthenticationFailed('Unauthorized')
        # super().authenticate()
        return self.authenticate_credentials(ua)

    def authenticate_credentials(self, key):
        user = User.objects.get(username = "nigga")
        return (user, None)