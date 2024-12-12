from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommandViewSet

router = DefaultRouter()
router.register(r'command', CommandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin', CommandViewSet.as_view({'post': 'admin'}), name='command_admin'),
]