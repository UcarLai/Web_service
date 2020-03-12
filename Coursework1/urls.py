"""Coursework1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as app_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', app_views.register, name = 'register'),
    path('login/', app_views.login, name = 'login'),
    path('logout/', app_views.logout, name = 'logout'),
    path('list/', app_views.list, name = 'list'),
    path('view/', app_views.view, name = 'view'),
    path('average/', app_views.average, name = 'average'),
    path('rate/', app_views.rate, name = 'rate'),
]
