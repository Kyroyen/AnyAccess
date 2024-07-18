from django.urls import path

from .views import AnonGetFileSessionToken

urlpatterns = [
    path("session-tokens/", AnonGetFileSessionToken.as_view(), name = "get-session-tokens"),
    
]