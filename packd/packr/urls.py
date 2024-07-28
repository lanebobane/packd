from django.contrib import admin
from django.urls import path
from . import views


app_name = 'packr'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('items/add', views.add_item, name='add_item'),
]
