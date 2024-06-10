from django.db.models import signals
from django.dispatch import receiver

from .models import UserFiles
from cloudinary_utils.cloudinary_upload import CloundiaryCustom

@receiver(signals.pre_save, sender = UserFiles)
def uploader( sender, instance, **kwargs):
    # print(instance)

    cloudinary_file = CloundiaryCustom.upload_file(
        instance.file_save.file.file,
        str(instance.file_name)
    )

    instance.file_url = cloudinary_file["secure_url"]
    instance.file_name = str(instance.file_save)

