from . import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    url('', views.register, name = 'register')
]