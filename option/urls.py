from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OptionViewSet


router = DefaultRouter()
router.register(r'option', OptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
]