from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from category.models import Category
from knowledge_base import settings

from .models import Command
from .serializers import CommandAdminSerializer, CommandSerializer
from rest_framework.views import APIView

class CommandViewSet(ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class CommandAdminViewSet(ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandAdminSerializer

    def perform_create(self, serializer):
        param = self.request.data.get('param', None)
            
        if param == settings.DIRECT_ACTIVATION_PASSWORD:
            serializer.save(active=True)
        else:
            raise ValidationError({"detail": "Wrong password"})

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class CommandsByCategoryViewSet(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": f"Category with ID {category_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        commands = Command.objects.filter(category=category)
        serializer = CommandSerializer(commands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)