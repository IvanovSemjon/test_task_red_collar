"""Views для HTML интерфейса."""
from django.shortcuts import render

def home_view(request):
    """Главная страница с картой."""
    return render(request, 'home.html')

def points_list_view(request):
    """Список точек."""
    return render(request, 'points_list.html')

def messages_list_view(request):
    """Список сообщений."""
    return render(request, 'messages_list.html')
