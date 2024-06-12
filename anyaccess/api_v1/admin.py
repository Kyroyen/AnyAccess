from django.contrib import admin
from .models import AppUser, UserFiles, FileSession


admin.site.register(AppUser)
admin.site.register(UserFiles)
admin.site.register(FileSession)
