from django.urls import path
from .views import CommandAdminViewSet, CommandViewSet

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
]