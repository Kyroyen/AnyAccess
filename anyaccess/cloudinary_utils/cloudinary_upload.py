from cloudinary.uploader import upload
from io import BytesIO

class CloundiaryCustom(object):

    @classmethod
    def upload_file(cls, file:BytesIO, file_name):
        file.name = file_name
        file_deets = upload(
            file,
            resource_type = "raw",
            folder="user/files",
        )

        # print(file_deets)
        return file_deets
