from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'description', 'image_preview']
    list_display_links = ['id', 'service']
admin.site.register(Service, ServiceAdmin)
