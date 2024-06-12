from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from .models import AppUser, UserFiles, FileSession
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

class UserFileUploadSerializer(serializers.ModelSerializer):
    # file_save = serializers.FileField(required = True, write_only = True,)

    class Meta:
        model = UserFiles
        fields = [
            "user",
            "origin",
            "file_save",
            "file_uuid",
            "file_name",
        ]
        extra_kwargs = {
            "user" : {
                "write_only" : True,
                "required" : True,
            },
            "origin" : {
                "required" : True,
            },
            "file_save" : {
                "required" : True,
                "write_only" : True,
            },
            "file_uuid" : {
                "read_only" : True,
            },
            "file_name" : {
                "read_only" : True,
            },
        }
    
    def to_internal_value(self, data):
        data["user"] = data.pop("user").pk
        temp = super().to_internal_value(data)
        print("tiv", temp)
        return temp
    
    def to_representation(self, instance):
        temp = super().to_representation(instance)
        print("to_repre", instance, temp)
        return temp
    
class UserFileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFiles
        fields = [
            "origin",
            "file_uuid",
            "file_name",
        ]


class FileSessionCreateSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(
        queryset = UserFiles.objects.all(),
        many = True,
    )

    class Meta:
        model = FileSession
        fields = [
            "user",
            "files",
            "session_id",
            "session_otp",
            "timeout",
        ]
        extra_kwargs = {
            "user" : {
                "required" : True,
                "write_only" : True,
            },
            "files" : {
                "required" : True,
            },
            "session_id" : {
                "read_only" : True,
            },
            "session_otp" : {
                "read_only" : True,
            },
        }
    
    def to_internal_value(self, data):
        data["user"] = data.pop("user").pk
        return super().to_internal_value(data)