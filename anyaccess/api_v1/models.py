from django.db import models
from django.conf import settings
from dropbox import Dropbox
from storages.backends.dropbox import DropboxStorage
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

from utils.get_uuid import get_unique_id
from utils.get_uuid import generate_otp
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

class FileSession(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="session_owner")
    files = models.ManyToManyField(UserFiles, related_name="files_included")
    session_id = models.UUIDField(default=get_unique_id, primary_key=True)
    session_otp = models.IntegerField(default=generate_otp)
    created_at = models.DateTimeField(auto_now=True)
    opened = models.BooleanField(default=False)
    timeout = models.TimeField(default=timezone.timedelta(minutes=10))

    class Meta:
        unique_together = ["user", "session_otp"]

    @property
    def timed_out(self):
        return (timezone.now() > self.created_at + self.timed_out)