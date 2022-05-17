"""Определение схемы URL для пользователей."""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # Включение URL фвторизации по умолчанию.
    # django.contrib.auth.urls - аунтефикационные адреса по умолчанию('login', 'logout' и тд)
    path('', include('django.contrib.auth.urls')),
    # Страница регистрации.
    path('register/', views.register, name='register'),
]