from rest_framework import serializers

from category.models import Category
from .models import Option


class OptionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Option
        fields = ['id', 'title', 'description', 'category', 'level', 'combinable', 'standalone', 'overwrite', 'active', 'created_at', 'updated_at']
        read_only_fields = ['active', 'created_at', 'updated_at']