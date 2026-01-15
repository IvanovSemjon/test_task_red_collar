"""Views для HTML интерфейса."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    """Главная страница с картой."""
    return render(request, 'home.html')

@login_required
def points_list_view(request):
    """Список точек."""
    return render(request, 'points_list.html')

@login_required
def messages_list_view(request):
    """Список сообщений."""
    return render(request, 'messages_list.html')
