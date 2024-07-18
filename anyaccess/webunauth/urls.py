from django.urls import path

from .views import AnonGetFileSessionToken, FileView

urlpatterns = [
    path("session-tokens/", AnonGetFileSessionToken.as_view(), name = "get-session-tokens"),
    path("files/", FileView.as_view({"post":"list", "get":"retrieve"}), name="files-view"),
    
]