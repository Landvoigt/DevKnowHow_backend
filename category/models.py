from django.db import models


class Category(models.Model):
    TYPE_CHOICES = [
        ('command', 'Command'),
        ('routine', 'Routine'),
        ('function', 'Function'),
    ]

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=10000, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='command')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
