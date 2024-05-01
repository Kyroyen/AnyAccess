from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode

from django.contrib.auth.models import User


# Create your views here.

class CustomAuth(BaseTokenAuthentication):

    decode_algo = ["HS256"]

    def authenticate(self, request):
        if 

        auth = request.META.get('HTTP_AUTHORIZATION').split()
        # print(auth)

        if len(auth) == 1:
            msg = ('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)
        
        secret_token = auth[1]

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