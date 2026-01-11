from rest_framework import serializers

from command.serializers import CommandSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'type', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']


class CategoryDetailSerializer(CategorySerializer):
    commands = CommandSerializer(many=True, read_only=True)

    def get_commands(self, obj):
        qs = obj.commands.filter(active=True)
        return CommandSerializer(qs, many=True).data

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['commands']
