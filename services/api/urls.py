from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ServiceViewSet


router = DefaultRouter()
router.register('services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),

]