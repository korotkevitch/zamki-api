from rest_framework import viewsets, mixins, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from articles.models import Article, Review
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsReviewUserOrReadOnly
from .serializers import ArticleSerializer, ArticleImageSerializer, ReviewSerializer
from rest_framework.decorators import action
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# from drf_spectacular.utils import (extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes,)


class ArticleViewSet(viewsets.ModelViewSet):
    """View for manage articles APIs."""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'upload_image':
            return ArticleImageSerializer

        return self.serializer_class


    @action(methods=['POST'], detail=True, url_path='upload-images')
    def upload_image(self, request, pk=None):
        """Upload an image to article."""
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    def get_queryset(self):
        rating = self.kwargs['rating']
        return Review.objects.filter(rating=rating)


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)  # для http://127.0.0.1:8000/reviews/?username=admin


class ReviewCreate(generics.CreateAPIView):
    """View for manage reviews APIs."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        article = Article.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(article=article, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("Вы уже оценивали эту статью!")

        if article.number_rating == 0:
            article.avg_rating = serializer.validated_data['rating']
        else:
            article.avg_rating = (article.avg_rating + serializer.validated_data['rating'])/2

        article.number_rating = article.number_rating + 1
        article.save()

        serializer.save(article=article, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(article=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'