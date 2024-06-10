from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from .models import AppUser
from authmoth.google_api import google_token_verify

class UserRegisterSerializer(serializers.ModelSerializer):
    google_id_token = serializers.CharField(write_only = True)

    class Meta:
        model = AppUser
        fields = (
            'email',
            'google_id_token',
            'first_name',
            'last_name',
            "username",
            "profile_photo",
            )
    
        extra_kwargs = {
            "email" : {
                "read_only" : True,
            },
            "first_name" : {
                "read_only" : True,
            },
            "last_name" : {
                "read_only" : True,
            },
            "profile_photo" : {
                "read_only" : True,
            },
            "google_id_token" : {
                "write_only" : True,
                "required" : True,
            },
            "username" : {
                "required" : True,
            }
        }
    
    def to_internal_value(self, data):

        final_data = {}
        token_data = google_token_verify(data.pop("google_id_token"))

        final_data["profile_photo"] = token_data.pop("picture")
        final_data["first_name"] = token_data.pop("given_name")
        final_data["last_name"] = token_data.pop("family_name")
        final_data["email"] = token_data.pop("email")

        final_data["username"] = data.pop("username")

        return final_data
    
    def validate(self, attrs):
        self.validate_username(attrs["username"])
        self.validate_email(attrs["email"])
        return super().validate(attrs)

    def validate_username(self, value):
        if self.Meta.model.objects.filter(username=value).exists():
            raise ValidationError("Username should be unique")
        return True
    
    def validate_email(self, value):
        if self.Meta.model.objects.filter(email=value).exists():
            raise ValidationError("Email should be unique")
        return True

