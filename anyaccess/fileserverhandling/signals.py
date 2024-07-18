from django.db.models import signals
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import asyncio
from time import time_ns
import threading

from api_v1.models import FileSession
from cloudinary_utils.download_cloudinary_file import cloudinary_file_downloader, FileDownloadData

@receiver(signals.pre_save, sender = FileSession)
def downloadWhenUpdated(sender, instance,  **kwargs):
    if instance.opened:
        print("Opened File Session")
        # print(instance.files.first().file_url, instance.files.first().file_uuid, instance.files.first().file_name)
        file_data = tuple(FileDownloadData(i.file_url, i.file_uuid, i.file_name) for i in instance.files.all())
        t1= threading.Thread(target=start_with_async_downloading, args=(file_data,))
        t1.start()
        # print(f"exited at: {time_ns()}")
    
def start_with_async_downloading(file_data):
    async_to_sync(cloudinary_file_downloader)(file_data)
    