from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommandCopyIncrementViewSet, CommandViewSet, CommandsByCategoryViewSet


router = DefaultRouter()
router.register(r'command', CommandViewSet, basename='command')
router.register(r'command', CommandCopyIncrementViewSet, basename='increment_copy')
router.register(r'command/category/(?P<category_id>\d+)', CommandsByCategoryViewSet, basename='commands-by-category')

urlpatterns = [
    path('', include(router.urls)),
]
