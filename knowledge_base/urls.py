from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', include('category.urls')),
    path('command/', include('command.urls')),
]
