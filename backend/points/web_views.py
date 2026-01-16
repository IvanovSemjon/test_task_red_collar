"""Views для HTML интерфейса."""
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import CustomUser

def home_view(request):
    """Главная страница с картой."""
    return render(request, 'home.html')

def points_list_view(request):
    """Список точек."""
    return render(request, 'points_list.html')

def messages_list_view(request):
    """Список сообщений."""
    return render(request, 'messages_list.html')

def register_view(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        username = request.POST.get('username')
        display_name = request.POST.get('display_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(username=username).exists():  # pylint: disable=no-member
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')
        
        CustomUser.objects.create_user(  # pylint: disable=no-member
            username=username,
            password=password,
            display_name=display_name
        )
        messages.success(request, f'Выживший {display_name} зарегистрирован! Используйте API для входа.')
        return redirect('home')
    
    return render(request, 'register.html')
