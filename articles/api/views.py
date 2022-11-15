from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from articles.models import Article
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsReviewUserOrReadOnly
from .serializers import ArticleSerializer, ArticleImageSerializer
from rest_framework.decorators import action
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