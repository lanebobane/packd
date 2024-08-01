from django.contrib import admin
from django.urls import path
from . import views


app_name = 'packr'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('items/add', views.add_item, name='add_item'),
    path('pack/add', views.add_pack, name='add_pack'),
    path('items/delete/(?P<pk>[0-9]+)/$', views.delete_item, name='delete_item'),
    path('pack/delete/(?P<pk>[0-9]+)/$', views.delete_pack, name='delete_pack'),
    path('pack/share/(?P<pk>[0-9]+)/$', views.share_pack, name='share_pack'),
    path('pack/adopt/(?P<pk>[0-9]+)/$', views.adopt_pack, name='adopt_pack'),
]
