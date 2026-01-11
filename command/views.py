import re
from django.db.models import Q
from django.db.models import F
from django.utils.translation import activate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from category.models import Category
from .models import Command
from .serializers import CommandSerializer


class BaseCommandViewSet(ModelViewSet):
    serializer_class = CommandSerializer

    def apply_search_filter(self, queryset):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            cleaned_query = search_query.replace('*', '')
            queryset = queryset.filter(
                Q(title__iregex=rf'{re.escape(cleaned_query)}') |
                Q(description__iregex=rf'{re.escape(cleaned_query)}')
            )
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
    

class CommandViewSet(BaseCommandViewSet):
    queryset = Command.objects.filter(active=True)
    
    def list(self, request, *args, **kwargs):
        lang = request.headers.get("Accept-Language", "en")
        activate(lang)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommandsByCategoryViewSet(BaseCommandViewSet):
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Command.objects.none()

        queryset = Command.objects.filter(category=category, active=True)
        return self.apply_search_filter(queryset)
    
    def list(self, request, *args, **kwargs):
        lang = request.headers.get("Accept-Language", "en")
        activate(lang)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CommandCopyIncrementViewSet(ViewSet):
    @action(detail=True, methods=['post'])
    def increment_copy(self, request, pk=None):
        try:
            command = Command.objects.get(pk=pk)
        except Command.DoesNotExist:
            return Response({"error": f"Command with id {pk} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        command.copy_count = F('copy_count') + 1
        command.save(update_fields=['copy_count'])

        command.refresh_from_db()
        
        return Response({"status": "copy count incremented", "copy_count": command.copy_count}, status=status.HTTP_200_OK)