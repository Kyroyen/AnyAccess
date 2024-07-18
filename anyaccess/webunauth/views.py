from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404

import jwt

from api_v1.models import AppUser, FileSession
from django.conf import settings

from .serializers import UnauthOTPSessionSerializer, OutViewFileListSerializer
from .CustomRateLimiter import WebUnauthThrottle


class AnonGetFileSessionToken(APIView):
    # throttle_classes = [WebUnauthThrottle]
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response()

    def post(self, request):
        username = request.data.get("username")
        session_otp = request.data.get("session_otp")
        # print(username, session_otp)

        if (session_otp is None) or (username is None):
            return Response(data={'error': "session_tp or username not found"}, status=403)
        data = {"user": username, "session_otp": session_otp}
        # print(data)
        serializer = UnauthOTPSessionSerializer()
        try:
            inst = serializer.get_valid_instance(data)
            # print(inst)
            # print(inst.user, str(inst.session_id), inst.timeout_at)
            session_token = jwt.encode(
                {"user": inst.user.username,
                 "session_uuid": str(inst.session_id),
                 "exp": inst.timeout_at
                 },
                settings.SECRET_KEY,

            )
            # print("token", session_token)
            return Response({"session_token": session_token}, status=202)
        except AppUser.DoesNotExist as e:
            # print("user")
            return Response(data={"error": "this user doesn't exists"}, status=400)
        except FileSession.DoesNotExist as e:
            # print(e)
            return Response(data={"error": "this session doesn't exists"}, status=400)
        except Exception as e:
            return Response(data={"error": e.args}, status=400)


class FileView(ViewSet):
    authentication_classes = []
    permission_classes = []

    def validate_token(self, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("expired")
            raise Exception("Already expired")
        except Exception:
            raise Exception("This token isn't valid anymore")

    def list(self, request):
        session_token = request.META.get("HTTP_AUTHORIZATION")
        print(session_token)
        if (session_token is None) or len(session_token.split(" ")) != 2:
            return Response({"error": "Send correct token with the request"}, status=403)

        try:
            payload = self.validate_token(session_token.split()[1])
        except:
            return Response({"error": "This token isn't valid"}, status=403)

        session = get_object_or_404(
            FileSession, session_id=payload["session_uuid"])
        files = session.files.all()

        serializer = OutViewFileListSerializer(files, many=True)

        return Response(data={"files": serializer.data}, status=200)

    def retrieve(self, request):
        session_token = request.META.get("HTTP_AUTHORIZATION")
        print(session_token)
        if (session_token is None) or len(session_token.split(" ")) != 2:
            return Response({"error": "Send correct token with the request"}, status=403)

        try:
            payload = self.validate_token(session_token.split()[1])
        except:
            return Response({"error": "This token isn't valid"}, status=403)

        session = get_object_or_404(
            FileSession, session_id=payload["session_uuid"])
        files = session.files.all()

        file_ind = request.GET.get("ind", 0)

        if int(file_ind) >= len(files):
            return Response({"error": "Indexing invalid"}, status=404)
        print()
        file = files[int(file_ind)]

        return FileResponse(
            open(
                settings.TEMP_FILE_URL.joinpath(
                    str(file.file_uuid)
                    ),
                "rb"
            ),
            # as_attachment=True,
            content_type = "application/zip",
            filename=file.file_name,
        )
