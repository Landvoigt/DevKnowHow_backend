from rest_framework import serializers
from category.models import Category
from .models import Command


class CommandSerializer(serializers.ModelSerializer):
    category = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Command
        fields = ['id', 'title', 'category', 'description', 'example', 'tooltip', 'options', 'alternatives', 'copy_count', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']

    def create(self, validated_data):
        categories = validated_data.pop("category", [])
        command = super().create(validated_data)
        command.category.set(categories)
        return command

    def update(self, instance, validated_data):
        categories = validated_data.pop("category", None)
        command = super().update(instance, validated_data)
        if categories is not None:
            command.category.set(categories)
        return command

    def validate_category(self, value_list):
        categories = []
        for value in value_list:
            if isinstance(value, Category):
                categories.append(value)
            elif isinstance(value, str):
                if value.isdigit():
                    try:
                        cat = Category.objects.get(id=int(value))
                        categories.append(cat)
                        continue
                    except Category.DoesNotExist:
                        pass
                cat, _ = Category.objects.get_or_create(title=value)
                categories.append(cat)
            elif isinstance(value, int):
                try:
                    cat = Category.objects.get(id=value)
                    categories.append(cat)
                except Category.DoesNotExist:
                    raise serializers.ValidationError(f"Category with ID {value} not found.")
            else:
                raise serializers.ValidationError("Invalid category value.")
        return categories

    def validate(self, attrs):
        attrs["category"] = self.validate_category(attrs.get("category"))
        return attrs
