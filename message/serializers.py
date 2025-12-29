from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']