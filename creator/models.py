from django.db import models


class Creator(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    email = models.CharField(max_length=256)