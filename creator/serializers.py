from rest_framework import serializers
from .models import Creator


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['id', 'firstName', 'lastName', 'email', 'active', 'created_at', 'updated_at',]
        read_only_fields = ['active', 'created_at', 'updated_at']