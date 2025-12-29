from rest_framework.viewsets import ModelViewSet
from .models import Option
from .serializers import OptionSerializer


class OptionViewSet(ModelViewSet):
    queryset = Option.objects.filter(active=True)
    serializer_class = OptionSerializer