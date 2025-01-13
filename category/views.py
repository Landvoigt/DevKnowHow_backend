from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True).prefetch_related('sub_categories')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


    # def get_queryset(self):
    #     queryset = Category.objects.filter(active=True).prefetch_related('subcategories')
    #     subcategory_title = self.request.query_params.get('subcategory', None)
    #     if subcategory_title:
    #         queryset = queryset.filter(subcategories__title__icontains=subcategory_title)
    #     return queryset

    # def perform_create(self, serializer):
    #     subcategories_data = self.request.data.get('subcategories', [])
    #     category = serializer.save()
    #     for subcategory_data in subcategories_data:
    #         category.subcategories.create(**subcategory_data)

    # def perform_update(self, serializer):
    #     subcategories_data = self.request.data.get('subcategories', [])
    #     category = serializer.save()
    #     category.subcategories.all().delete()  # Clear existing subcategories
    #     for subcategory_data in subcategories_data:
    #         category.subcategories.create(**subcategory_data)