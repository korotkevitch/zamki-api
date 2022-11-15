from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'storyline', 'text', 'service', 'active', 'avg_rating', 'number_rating', 'created']
    list_display_links = ['title']
admin.site.register(Article, ArticleAdmin)
