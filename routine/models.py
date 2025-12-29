from django.db import models
from category.models import Category


class Routine(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, unique=True)
    routine = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="routines")
    example = models.CharField(max_length=2000, blank=True, null=True)
    tooltip = models.CharField(max_length=1000, blank=True, null=True)
    alternative = models.ManyToManyField("self", symmetrical=False, related_name="alternative_to", blank=True)

    copy_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def increment_copy_count(self):
        self.copy_count += 1
        self.save()