import re
from django.db.models import Q
from django.utils.translation import activate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from category.models import Category
from .models import Routine
from .serializers import RoutineSerializer


class BaseRoutineViewSet(ModelViewSet):
    serializer_class = RoutineSerializer

    def apply_search_filter(self, queryset):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            cleaned_query = search_query.replace('*', '')
            queryset = queryset.filter(
                Q(title__iregex=rf'{re.escape(cleaned_query)}') |
                Q(routine__iregex=rf'{re.escape(cleaned_query)}')
            )
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
    

class RoutineViewSet(BaseRoutineViewSet):
    queryset = Routine.objects.all()

    def get_queryset(self):
        queryset = Routine.objects.filter(active=True)
        return self.apply_search_filter(queryset)

    def list(self, request, *args, **kwargs):
        lang = request.headers.get("Accept-Language", "en")
        activate(lang)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class RoutinesByCategoryViewSet(BaseRoutineViewSet):
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Routine.objects.none()

        queryset = Routine.objects.filter(category=category, active=True)
        return self.apply_search_filter(queryset)
    
    def list(self, request, *args, **kwargs):
        lang = request.headers.get("Accept-Language", "en")
        activate(lang)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RoutineCopyIncrementViewSet(ViewSet):
    @action(detail=True, methods=['post'])
    def increment_copy(self, request, pk=None):
        try:
            routine = Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            return Response({"error": f"Routine with id {pk} not found."}, 
                status=status.HTTP_404_NOT_FOUND)
        
        routine.increment_copy_count()
        
        return Response({"status": "copy count incremented", "copy_count": routine.copy_count}, 
            status=status.HTTP_200_OK)