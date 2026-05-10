from rest_framework.viewsets import ModelViewSet
from .models import Option
from .serializers import OptionSerializer


class OptionViewSet(ModelViewSet):
    queryset = Option.objects.filter(active=True).select_related("command").prefetch_related("category")
    serializer_class = OptionSerializer
