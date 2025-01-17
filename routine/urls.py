from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoutineCopyIncrementViewSet, RoutineViewSet, RoutinesByCategoryViewSet


router = DefaultRouter()
router.register(r'routine', RoutineViewSet, basename='routine')
router.register(r'routine', RoutineCopyIncrementViewSet, basename='increment_copy')
router.register(r'routine/category/(?P<category_id>\d+)', RoutinesByCategoryViewSet, basename='routines-by-category')

urlpatterns = [
    path('', include(router.urls)),
]
