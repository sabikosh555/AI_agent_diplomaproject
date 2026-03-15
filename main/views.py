"""
Main app - function-based views
"""
from django.shortcuts import render


def index_view(request):
    """Главная страница сайта."""
    return render(request, 'main/index.html')
