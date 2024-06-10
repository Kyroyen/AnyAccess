"""
WSGI config for anyaccess project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()

from django.core.wsgi import get_wsgi_application

cloudinary.config( 
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
  api_key = os.environ.get("CLOUDINARY_API_KEY"),
  api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
  secure = True
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anyaccess.settings')

application = get_wsgi_application()
