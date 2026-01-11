from rest_framework import serializers

from option.serializers import OptionSerializer
from .models import Command


class CommandSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    option = OptionSerializer(many=True, read_only=True)
    alternative = serializers.SerializerMethodField()
    
    class Meta:
        model = Command
        fields = ['id', 'title', 'category', 'description', 'example', 'tooltip', 'option', 'alternative', 'copy_count', 'active', 'created_at', 'updated_at']
        read_only_fields = ['active', 'created_at', 'updated_at']

    def get_alternative(self, obj):
        return CommandAlternativeSerializer(
            obj.alternative.all(),
            many=True,
            context=self.context
        ).data

class CommandAlternativeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Command
        fields = ['id', 'title', 'category', 'description', 'example', 'tooltip', 'option', 'copy_count', 'active', 'created_at', 'updated_at']
        read_only_fields = ['active', 'created_at', 'updated_at']
