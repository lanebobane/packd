from django.contrib import admin
from .models import Trip, Bag, Item


admin.site.site_header = 'Packd Header Placeholder'
admin.site.site_title = 'Packd Website Title Placeholder'
admin.site.index_title = 'Packd Index Title Placeholder'


# Register your models here.
admin.site.register(Trip)
admin.site.register(Bag)
admin.site.register(Item)