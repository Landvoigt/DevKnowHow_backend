from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet

from knowledge_base import settings

from .models import Command
from .serializers import CommandAdminSerializer, CommandSerializer


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
