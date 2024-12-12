from django.contrib import admin
from django.urls import path
from category.views import get

urlpatterns = [
    path('', get),
]
