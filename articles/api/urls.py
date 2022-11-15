from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ReviewList, ReviewDetail, ReviewCreate, UserReview, RatingReview


router = DefaultRouter()
router.register('article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    path('reviews/<int:rating>/', RatingReview.as_view(), name='rating-review-detail'),  # /reviews/4/ - with rating 4
    path('reviews/', UserReview.as_view(), name='user-review-detail'),  # /reviews/?username=admin - reviews from admin

]