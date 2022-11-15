from rest_framework import serializers
from service.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for service."""
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image']
        read_only_fields = ['id']


class ServiceImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to services."""

    class Meta:
        model = Service
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}