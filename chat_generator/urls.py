from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-chat', views.generate_chat, name='generate-chat'),
]