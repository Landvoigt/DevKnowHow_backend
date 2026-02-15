from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from .views import SearchView


def api_root(request):
    return JsonResponse({"message": "DevKnowHow_backend API is running."})

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),
    path('', include('category.urls')),
    path('', include('command.urls')),
    path('', include('routine.urls')),
    path('', include('option.urls')),
    path('', include('creator.urls')),
    path('', include('message.urls')),
]
