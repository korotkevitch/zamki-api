from django.contrib import admin
from .models import Article, Review


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'related_service', 'storyline', 'text', 'image_preview', 'user', 'active', 'avg_rating', 'number_rating',
                    'created', 'updated']
admin.site.register(Article, ArticleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'review_user', 'description', 'rating', 'created', 'updated', 'active']
    list_display_links = ['id', 'article']
admin.site.register(Review, ReviewAdmin)
