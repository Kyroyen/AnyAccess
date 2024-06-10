from django.db import models
from django.conf import settings
from dropbox import Dropbox
from storages.backends.dropbox import DropboxStorage
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from utils.get_uuid import get_unique_id

from .CustomStorage import FakeStorage

class AppUser(AbstractUser, PermissionsMixin):
    profile_photo = models.URLField(default=settings.DEFAULT_PROFILE_PIC)
    class Meta(object):
        unique_together = ("email",)

OAUTH_token = "sl.B1nKbebSOcUwSF86BDatz5gooZolcTqFLrXlsfemNC18YztYnJx5u_Yr1ilAqzOONoRw2cGxVoMKkjkyY-Sbkwnr5_z-h_Oo2p5VHmEqlWMtPfwQEGjn5JYdIlDZfy8rcmqsgu3fs2WY2enn0hMg"

class UserFiles(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, related_name="file_user")
    origin = models.CharField(max_length=4, choices=settings.FILE_ORIGINS)
    file_save = models.FileField(null=True, default="Saved to Dropbox", blank=True)
    file_uuid = models.UUIDField(default=get_unique_id, primary_key=True)
    file_url = models.URLField(blank=True)
    file_name = models.CharField(max_length=40, null=True, blank=True)

    def save(self,  *args, **kwargs) -> None:

        self.file_save.storage = FakeStorage()

        return super().save(*args, **kwargs)
        

