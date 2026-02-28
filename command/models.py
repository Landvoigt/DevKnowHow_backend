from django.db import models
from django.contrib.postgres.fields import ArrayField
from category.models import Category


class Command(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=2000, unique=True)
    description = models.TextField(max_length=10000, blank=True, null=True)
    context = models.CharField(max_length=50, blank=True, null=True)
    context_description = models.CharField(max_length=2000, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="commands")
    example = ArrayField(models.CharField(max_length=2000), blank=True, default=list)
    tooltip = models.CharField(max_length=1000, blank=True, null=True)
    alternative = models.ManyToManyField("self", symmetrical=False, related_name="alternative_to", blank=True)
    
    copy_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
        