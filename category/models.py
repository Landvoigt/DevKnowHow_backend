from django.utils import timezone
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=700, blank=True, null=True)
    active = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title