from rest_framework import serializers

from .models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ["active", "creation_date"]


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'active', 'title', 'description', 'sub_categories', 'creation_date']
        read_only_fields = ["active", "creation_date"]