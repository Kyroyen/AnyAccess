from rest_framework import serializers
from asgiref.sync import async_to_sync

from api_v1.models import FileSession, AppUser

class UnauthOTPSessionSerializer(object):
    
    def get_instance_thunder(self, data):
        user = data["user"]
        print("git")
        session_otp = data["session_otp"]
        queryset = AppUser.objects.get(username = user)
        if queryset is None:
            raise AppUser.DoesNotExist
        print(queryset)
        queryset = queryset.session_owner.filter(session_otp = session_otp).first()
        if queryset is None:
            raise FileSession.DoesNotExist
        print(queryset)
        return queryset
    
    def get_valid_instance(self, data):
        instance = self.get_instance_thunder(data)
        # print("whu--------t",instance.created_at)
        # print("whut",instance.timed_out)
        
        if instance.timed_out or instance.opened:
            raise Exception("This session doesn't exists or has timed out")
        
        instance.opened = True
        
        async_to_sync(instance.asave)()
                
        return instance
        
    

    
