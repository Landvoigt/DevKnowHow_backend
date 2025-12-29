from rest_framework.viewsets import ModelViewSet
from .models import Creator
from .serializers import CreatorSerializer


class CreatorViewSet(ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer