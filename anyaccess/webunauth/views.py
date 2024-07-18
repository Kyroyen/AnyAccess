from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt

from api_v1.models import AppUser, FileSession
from django.conf import settings

from .serializers import UnauthOTPSessionSerializer
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
            return Response({"session_token" : session_token}, status=202)
        except AppUser.DoesNotExist as e:
            # print("user")
            return Response(data={"error": "this user doesn't exists"}, status=400)
        except FileSession.DoesNotExist as e:
            # print(e)
            return Response(data={"error": "this session doesn't exists"}, status=400)
        except Exception as e:
            return Response(data={"error": e.args}, status=400)

        return Response()
