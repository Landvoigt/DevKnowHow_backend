from django.utils.translation import activate
from rest_framework.viewsets import ModelViewSet
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        lang = self.request.headers.get("Accept-Language", "en")
        activate(lang)
        return Category.objects.filter(active=True).prefetch_related('sub_categories')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        lang = self.request.headers.get("Accept-Language", "en")
        activate(lang)
        return SubCategory.objects.filter(active=True)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
