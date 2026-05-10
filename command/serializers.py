from rest_framework import serializers

from option.serializers import OptionSerializer
from .models import Command


class CommandBaseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Command
        fields = ['id', 'title', 'description', 'context', 'context_description', 'category', 'example', 'tooltip', 'option', 'tag', 'copy_count', 'active', 'created_at', 'updated_at']
        read_only_fields = ['active', 'created_at', 'updated_at']


class CommandSerializer(CommandBaseSerializer):
    alternative = CommandBaseSerializer(many=True, read_only=True)
    equivalent = CommandBaseSerializer(many=True, read_only=True)

    class Meta(CommandBaseSerializer.Meta):
        fields = CommandBaseSerializer.Meta.fields + [
            'alternative',
            'equivalent',
        ]
