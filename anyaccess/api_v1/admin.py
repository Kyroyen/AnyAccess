from django.contrib import admin
from .models import AppUser, UserFiles


admin.site.register(AppUser)
admin.site.register(UserFiles)

# Register your models here.
