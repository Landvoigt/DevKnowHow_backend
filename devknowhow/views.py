from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from typing import List

from command.models import Command
from command.serializers import CommandSerializer
from category.models import Category
from category.serializers import CategorySerializer


class SearchResult:
    def __init__(self, command: List[dict], category: List[dict]):
        self.command = command
        self.category = category
        self.command_count = len(command)
        self.category_count = len(category)
        self.total_count = self.command_count + self.category_count

    def to_dict(self):
        return {
            "command": self.command,
            "category": self.category,
            "counts": {
                "command": self.command_count,
                "category": self.category_count,
                "total": self.total_count
            }
        }


class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response(SearchResult([], []).to_dict())

        try:
            cleaned_query = query

            command_qs = Command.objects.filter(
                active=True
            ).filter(
                Q(title__icontains=cleaned_query) |
                Q(description__icontains=cleaned_query) |
                Q(category__title__icontains=cleaned_query) |
                Q(category__description__icontains=cleaned_query)
            ).distinct()

            category_qs = Category.objects.filter(
                active=True
            ).filter(
                Q(title__icontains=cleaned_query) |
                Q(description__icontains=cleaned_query)
            ).distinct()

            command_serialized = CommandSerializer(command_qs, many=True, context={'request': request}).data
            category_serialized = CategorySerializer(category_qs, many=True, context={'request': request}).data

            search_result = SearchResult(command_serialized, category_serialized)
            return Response(search_result.to_dict())
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
