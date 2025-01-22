from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', views.github_webhook, name='github_webhook'),
    path('', include('category.urls')),
    path('', include('command.urls')),
    path('', include('routine.urls')),
]
