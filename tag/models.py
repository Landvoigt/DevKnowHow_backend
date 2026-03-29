from django.db import models


class Tag(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
