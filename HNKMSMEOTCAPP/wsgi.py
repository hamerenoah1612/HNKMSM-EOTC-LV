"""
WSGI config for HNKMSMEOTCAPP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HNKMSMEOTCAPP.settings')

# application = get_wsgi_application()


import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HNKMSMEOTCAPP.settings')

application = get_wsgi_application()
application = WhiteNoise(application) # Add this line
application.add_files(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')) # For serving static files in production