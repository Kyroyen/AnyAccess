from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.utils import IntegrityError

from .serializers import UserRegisterSerializer

# Create your views here.

class hello_world(APIView):

    # authentication_classes = (CustomAuth, )

    def get(self, request):
        print(request.user, request.auth)
        return Response(data = {"hi" : "hello world"})
    
    def post(self, request):
        print(request.data)
        return Response()
    
class RegisterAppUserView(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserRegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=201)

        return Response(data = serializer.errors, status=403)
