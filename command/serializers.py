from rest_framework import serializers
from category.models import Category
from .models import Command

class CommandSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Command
        fields = '__all__'
        read_only_fields = ["active", "creation_date"]

    def validate_category(self, value):
        if isinstance(value, str):
            category, created = Category.objects.get_or_create(title=value)
            return category
        elif value.isdigit():
            try:
                category = Category.objects.get(id=int(value))
                return category
            except Category.DoesNotExist:
                raise serializers.ValidationError(f"Category with ID {value} not found.")
        raise serializers.ValidationError("Category must be a string or a valid category ID.")


# class CommandAdminSerializer(serializers.ModelSerializer):
#     category = serializers.CharField()

#     class Meta:
#         model = Command
#         fields = '__all__'
#         read_only_fields = ["active", "creation_date"]

#     def validate_category(self, value):
#         if isinstance(value, str):
#             category, created = Category.objects.get_or_create(title=value)
#             if created:
#                 category.active = True
#                 category.save()
#             return category
#         elif value.isdigit():
#             try:
#                 category = Category.objects.get(id=int(value))
#                 return category
#             except Category.DoesNotExist:
#                 raise serializers.ValidationError(f"Category with ID {value} not found.")
#         raise serializers.ValidationError("Category must be a string or a valid category ID.")