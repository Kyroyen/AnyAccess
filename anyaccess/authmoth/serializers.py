from typing import Any, Dict
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, update_last_login
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, Token, SlidingToken
from typing import Dict, Any
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import ValidationError
import json

from .google_api import google_token_verify
from exceptions.google_api_exceptions import GoogleAPITokenException

class GoogleOAuthTokenObtainSerializer(TokenObtainSerializer):
    
    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        self.fields["google_oauth_token"] = serializers.CharField(write_only = True)

    # def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
    #     print("obtain valid", attrs)
    #     return super().validate(attrs)

    
class GoogleOAuthTokenObtainPairSerializer(GoogleOAuthTokenObtainSerializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs) -> None:
        # print("GoogleOAuthTokenObtainPairSerializer")
        super().__init__(*args, **kwargs)


    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        print("GoogleOAuthTokenObtainPairSerializer valid", attrs)
        try:
            google_token = attrs["google_oauth_token"]
        except KeyError:
            pass
            
        # print(request)

        # try:
        #     request_data = json.loads(request)
        # except json.JSONDecodeError:
        #     raise ValidationError("can't decode")


        try:
            user_details = google_token_verify(google_token)
            self.user = get_user_model().objects.get(email = user_details["email"])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        except KeyError:
            raise exceptions.AuthenticationFailed("It should include a google_oauth_token")
        except GoogleAPITokenException as gae:
            print(gae.get_full_details())
            raise exceptions.AuthenticationFailed("Can't verify token! :(")

        refresh = self.get_token(self.user)
        data = {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token),
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    

# class GoogleOAuthObtainPairSerializer(TokenObtainPairSerializer):
#     required_params = {"google_oauth_"}

#     def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
#         try:
#             request = self.context["request"]
#         except KeyError:
#             pass

#         try:
#             request_data = json.loads(request)

