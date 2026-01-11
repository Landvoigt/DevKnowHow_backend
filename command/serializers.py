from rest_framework import serializers
from .models import Command


class CommandSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    
    class Meta:
        model = Command
        fields = ['id', 'title', 'category', 'description', 'example', 'tooltip', 'option', 'alternative', 'copy_count', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']
