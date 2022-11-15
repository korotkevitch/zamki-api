from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'related_service', 'storyline', 'text', 'active', 'avg_rating', 'number_rating', 'created']
admin.site.register(Article, ArticleAdmin)
