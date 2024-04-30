"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app.views import index, topbar, sidebar, chat, profile
from authentication.views import login, callback, logout, remove_session


urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('admin/', admin.site.urls),
    path('remove_session/', remove_session, name='remove_session'),
	path('topbar/', topbar, name='topbar'),
	path('sidebar/', sidebar, name='sidebar'),
	path('chat/', chat, name='chat'),
	path('profile/', profile, name='profile'),
]
