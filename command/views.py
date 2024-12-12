from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .models import Command
from .serializers import CommandSerializer
from category.models import Category


def get_or_create_category(category_title: str, is_admin: bool = False):
    """
    Helper function to retrieve or create a category.
    If it's an admin request, the category will be created with active=True.
    For normal requests, the category will be created with active=False.
    """
    if not category_title:
        return None, "Category title must be provided."

    active_status = True if is_admin else False
    category, created = Category.objects.get_or_create(
        title=category_title, defaults={"active": active_status}
    )

    return category, None if category else "Category creation failed."

class CommandViewSet(ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    def perform_create(self, serializer):
        category_title = self.request.data.get('category')

        if not category_title:
            return Response({"error": "Category title must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    
        category, error = get_or_create_category(category_title, is_admin=False)
        
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        if category:
            serializer.save(category=category, active=False)

    @action(detail=False, methods=['post'], url_path='admin')
    def admin(self, request):
        password = request.data.get("param")
        if password != settings.DIRECT_ACTIVATION_PASSWORD:
            return Response({"error": "Invalid password"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data.pop("param", None)

        category_title = data.get('category')

        category, error = get_or_create_category(category_title, is_admin=True)

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        data['category'] = category.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(active=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)