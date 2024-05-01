from django.urls import path
from .views import hello_world

urlpatterns = [
    path("hello/", hello_world.as_view(), name = "hello-world"),
    
]