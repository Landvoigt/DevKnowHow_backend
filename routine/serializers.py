from rest_framework import serializers
from category.models import Category, SubCategory
from .models import Routine


class RoutineSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    sub_category = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Routine
        fields = '__all__'
        read_only_fields = ["active", "creation_date"]

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

    def validate_sub_category(self, value):
        if not value:
            return None

        category = self.initial_data.get("category")
        if isinstance(category, str):
            category, _ = Category.objects.get_or_create(title=category)
        elif category.isdigit():
            try:
                category = Category.objects.get(id=int(category))
            except Category.DoesNotExist:
                raise serializers.ValidationError(f"Category with ID {category} not found.")
        else:
            raise serializers.ValidationError("Invalid category format.")

        sub_category, _ = SubCategory.objects.get_or_create(
            title=value, 
            category=category
        )
        return sub_category
    
    def validate(self, attrs):
        attrs["category"] = self.validate_category(attrs.get("category"))
        attrs["sub_category"] = self.validate_sub_category(attrs.get("sub_category"))
        return attrs
