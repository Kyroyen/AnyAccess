import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List

from django.conf import settings
from time import time_ns

class FileDownloadData:
    def __init__(self, file_url, file_uuid, file_name):
        self.file_url = file_url
        self.file_uuid = file_uuid
        self.file_name = file_name

async def cloudinary_file_downloader(file_data:List[FileDownloadData]):
    
    def get_response_and_save(file_info:FileDownloadData):
        res = requests.get(file_info.file_url)
        with open(settings.TEMP_FILE_URL.joinpath(str(file_info.file_uuid)), "wb") as f:
            f.write(res.content)
            
    
    with ThreadPoolExecutor(3) as three:
        three.map(get_response_and_save, file_data)
    
    
    