from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategoryDetailSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(active=True).prefetch_related('commands')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer