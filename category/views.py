from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from .models import Category
from .serializers import CategoryDetailSerializer, CategorySerializer
from command.models import Command

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(active=True).prefetch_related(
        Prefetch(
            'commands',
            queryset=Command.objects.filter(active=True)
        )
    )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer