from rest_framework.views import APIView
from rest_framework.response import Response

from authmoth.custom_auth import CustomAuth

# Create your views here.

class hello_world(APIView):

    authentication_classes = (CustomAuth, )

    def get(self, request):
        print(request.user, request.auth)
        return Response(data = {"hi" : "hello world"})
    
    def post(self, request):
        print(request.data)
        return Response()