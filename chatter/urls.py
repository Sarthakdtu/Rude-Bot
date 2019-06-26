from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/<str:username>',views.chat, name='chat'),
    path('error', views.error, name='error'),
]
