from django.urls import path
from .views import hello_world, RegisterAppUserView

urlpatterns = [
    path("hello/", hello_world.as_view(), name = "hello-world"),
    path("register/", RegisterAppUserView.as_view(), name = "register-view"),
]