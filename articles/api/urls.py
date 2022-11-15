from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet


router = DefaultRouter()
router.register('article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),

]