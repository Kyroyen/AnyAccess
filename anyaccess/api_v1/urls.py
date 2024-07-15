from django.urls import path
from .views import RegisterAppUserView, UserFileUploadView, UserFilesViewSet, FileSessionViewSet

urlpatterns = [
    path("register/", RegisterAppUserView.as_view(), name = "register-view"),

    path("files-upload/", UserFileUploadView.as_view({"post":"create"}), name = "user-files"),
    path("files/", UserFilesViewSet.as_view({"post":"list", "get":"retrieve"}), name = "file-view"),

    path("session/", FileSessionViewSet.as_view({"post":"create", "get":"retrieve", "put":"list"}), name="user-sessions"),

]