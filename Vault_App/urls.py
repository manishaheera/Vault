from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('user/login', views.user_login),
    path('user/logout', views.user_logout),

    path('user/dashboard',views.user_dashboard),
]