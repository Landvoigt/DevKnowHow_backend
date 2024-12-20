from django.urls import path
from .views import CommandAdminViewSet, CommandViewSet, CommandsByCategoryViewSet

urlpatterns = [
    path('', CommandViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
        'retrieve': 'retrieve'
    }), name='command-list'),

    path('admin/', CommandAdminViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
        'retrieve': 'retrieve'
    }), name='command-admin'),

    path('category/<int:category_id>/', CommandsByCategoryViewSet.as_view(), name='commands-by-category'),
]