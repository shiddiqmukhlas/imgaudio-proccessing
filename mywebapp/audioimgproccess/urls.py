from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('resize_image/', views.resize_image, name='resize_image'),
    path('compress_audio/', views.compress_audio, name='compress_audio'),
]

