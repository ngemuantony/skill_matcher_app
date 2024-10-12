from django.urls import path, include
from django.conf import settings
from accounts import views as user_view
from django.contrib.auth import views as auth
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', user_view.Login, name='login'),
    path('register/', user_view.register, name='register'),
    path('logout/', auth.LogoutView.as_view(next_page='login'), name='logout'),
]
