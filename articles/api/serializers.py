from rest_framework import serializers
from articles.models import Article, Review


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for article."""
    class Meta:
        model = Article
        fields = ['id', 'title', 'related_service', 'storyline', 'text', 'image', 'user', 'active', 'avg_rating',
                  'number_rating', 'created', 'updated']
        read_only_fields = ['id']


class ArticleImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to articles."""

    class Meta:
        model = Article
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('article',)