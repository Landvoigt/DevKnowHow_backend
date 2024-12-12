from rest_framework import serializers

from .models import Command


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = '__all__'
        read_only_fields = ["active", "creation_date"]