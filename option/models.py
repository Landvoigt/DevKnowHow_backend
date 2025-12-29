from django.db import models


class Option(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)