from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image_preview']
    list_display_links = ['id', 'name']
admin.site.register(Service, ServiceAdmin)
