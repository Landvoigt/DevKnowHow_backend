from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommandCopyIncrementViewSet, CommandViewSet


router = DefaultRouter()
router.register(r'command', CommandViewSet, basename='command')
router.register(r'command', CommandCopyIncrementViewSet, basename='increment_copy')

urlpatterns = [
    path('', include(router.urls)),
]
