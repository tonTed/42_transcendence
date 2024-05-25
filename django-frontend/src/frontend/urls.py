from django.urls import path
from frontend.views import index, login_password

urlpatterns = [
	path('', index, name='index'),
	path('login/password/', login_password, name='login_password'),
]
