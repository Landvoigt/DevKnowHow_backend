from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from category.models import Category
from .models import Routine
from .serializers import RoutineSerializer


class RoutineViewSet(ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class RoutinesByCategoryViewSet(ModelViewSet):
    serializer_class = RoutineSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Routine.objects.none()

        return Routine.objects.filter(category=category, active=True)
    
    def list(self, request, *args, **kwargs):
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