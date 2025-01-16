from django.db import IntegrityError
from rest_framework import serializers

from .models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ["active", "creation_date"]

    def create(self, validated_data):
        try:
            return SubCategory.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("SubCategory with this name already exists.")


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'active', 'title', 'description', 'sub_categories', 'creation_date']
        read_only_fields = ["active", "creation_date"]

    def get_sub_categories(self, obj):
        active_subcategories = obj.sub_categories.filter(active=True)
        return SubCategorySerializer(active_subcategories, many=True).data
    
    def create(self, validated_data):
        try:
            return Category.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Category with this name already exists.")