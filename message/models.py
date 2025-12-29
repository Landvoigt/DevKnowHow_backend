from django.db import models


class Message(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.TextField(max_length=10000, blank=True, null=True)