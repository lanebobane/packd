from django.contrib import admin
from django.urls import path
from . import views


app_name = 'packr'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('items/add', views.add_item, name='add_item'),
    path('items/delete/(?P<pk>[0-9]+)/$', views.delete_item, name='delete_item')

]
