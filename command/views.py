from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action

from category.models import Category

from .models import Command
from .serializers import CommandSerializer


class CommandViewSet(ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class CommandsByCategoryViewSet(ModelViewSet):
    serializer_class = CommandSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Command.objects.none()

        return Command.objects.filter(category=category, active=True)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CommandCopyIncrementViewSet(ViewSet):
    @action(detail=True, methods=['post'])
    def increment_copy(self, request, pk=None):
        try:
            command = Command.objects.get(pk=pk)
        except Command.DoesNotExist:
            return Response({"error": f"Command with id {pk} not found."}, 
                status=status.HTTP_404_NOT_FOUND)
        
        command.increment_copy_count()
        
        return Response({"status": "copy count incremented", "copy_count": command.copy_count}, 
            status=status.HTTP_200_OK)