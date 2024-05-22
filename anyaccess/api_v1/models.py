from django.db import models
from django.conf import settings
from dropbox import Dropbox
from storages.backends.dropbox import DropboxStorage
from utils.get_uuid import get_unique_id
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class AppUser(AbstractUser, PermissionsMixin):
    profile_photo = models.URLField(default=settings.DEFAULT_PROFILE_PIC)
    class Meta(object):
        unique_together = ("email",)

OAUTH_token = "sl.B1nKbebSOcUwSF86BDatz5gooZolcTqFLrXlsfemNC18YztYnJx5u_Yr1ilAqzOONoRw2cGxVoMKkjkyY-Sbkwnr5_z-h_Oo2p5VHmEqlWMtPfwQEGjn5JYdIlDZfy8rcmqsgu3fs2WY2enn0hMg"

class UserFiles(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True)
    origin = models.CharField(max_length=4, choices=settings.FILE_ORIGINS)
    file_url = models.FileField(null=True, default="Saved to Dropbox", blank=True)
    file_name = models.UUIDField(auto_created=True)

    def save(self, *args, **kwargs) -> None:
        print("fwfw",*args, **kwargs)
        # dbx = Dropbox(OAUTH_token).files_upload(self.file_url.read(), path = "/nigga/lola.txt")

        return super().save(*args, **kwargs)

