from django.utils import timezone
from django.db import models

from category.models import Category


class Command(models.Model):
    command = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="command")
    sub_category = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=10000)
    example = models.TextField(max_length=2000, blank=True, null=True)
    param = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
    creator_name = models.CharField(max_length=255)
    creator_email = models.CharField(max_length=255)
    creator_message = models.CharField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.command
