from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .serializers import UserRegisterSerializer, UserFileUploadSerializer, UserFileDataSerializer, FileSessionCreateSerializer
    
class RegisterAppUserView(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserRegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=201)

        return Response(data = serializer.errors, status=403)
    
class UserFileUploadView(ViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [BasicAuthentication]
    serializer_class = UserFileUploadSerializer

    def create(self, request):
        data = {}
        data["user"] = request.user
        data["origin"] = request.data.get("origin")
        data["file_save"] = request.data.get("file_save")
        if (data["file_save"] is None) or (data["file_save"] is None):
            return Response(data={"error" : "check the request"}, status=400)
        print(data)
        serializer = UserFileUploadSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=400)

class UserFilesViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = UserFileDataSerializer

    def retrieve(self, request):
        file_uuid = request.GET.get("file_uuid")
        if file_uuid is None:
            return Response(data = {"error" : "Enter File UUID"}, status=400)
        inst = request.user.file_user.get(pk = file_uuid)
        serializer = self.serializer_class(inst)
        return Response(data = serializer.data, status = 200)
    
    def list(self, request):
        queryset = request.user.file_user.all()
        serializer = self.serializer_class(queryset, many = True)
        return Response(data = serializer.data, status = 200)
    
class FileSessionViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = FileSessionCreateSerializer

    def create(self, request):
        data = request.data
        data["user"] = request.user
        # print(data)
        
        serialzier = self.serializer_class(data = data)
        if serialzier.is_valid():
            # print(serialzier.validated_data)
            serialzier.save()
            return Response(data = serialzier.data, status=201)
        
        return Response(data = serialzier.errors, status = 400)
    
    def retrieve(self, request):
        session_id = request.GET.get("session_id")
        queryset = request.user.session_owner.filter(session_id = session_id).first()
        serializer = self.serializer_class(queryset)
        return Response(data = serializer.data, status = 200)
    
    def list(self, request):
        queryset = request.user.session_owner.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)

