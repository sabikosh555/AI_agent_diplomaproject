"""
ASGI config for AI University project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_university.settings')

application = get_asgi_application()
