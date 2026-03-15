"""
WSGI config for AI University project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_university.settings')

application = get_wsgi_application()
