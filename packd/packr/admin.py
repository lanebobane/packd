from django.contrib import admin
from .models import Item, Pack


admin.site.site_header = 'Packd Header Placeholder'
admin.site.site_title = 'Packd Website Title Placeholder'
admin.site.index_title = 'Packd Index Title Placeholder'


# Register your models here.
admin.site.register(Pack)
admin.site.register(Item)