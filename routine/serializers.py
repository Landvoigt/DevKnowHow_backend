from rest_framework import serializers
from category.models import Category
from .models import Routine


class RoutineSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Routine
        fields = ['id', 'title', 'routine', 'category', 'example', 'tooltip', 'alternative', 'copy_count', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']

    def validate_category(self, value):
        if isinstance(value, Category):
            return value
        if isinstance(value, str):
            category, _ = Category.objects.get_or_create(title=value)
            return category
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
            try:
                category = Category.objects.get(id=int(value))
                return category
            except Category.DoesNotExist:
                raise serializers.ValidationError(f"Category with ID {value} not found.")
        raise serializers.ValidationError("Category must be a string or a valid category ID.")
    
    def validate(self, attrs):
        attrs["category"] = self.validate_category(attrs.get("category"))
        return attrs
