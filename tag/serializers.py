from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'active', 'created_at', 'updated_at']
        read_only_fields = ['active', 'created_at', 'updated_at']