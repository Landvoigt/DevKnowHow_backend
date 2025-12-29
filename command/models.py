from django.db import models
from category.models import Category
from option.models import Option


class Command(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=2000, unique=True)
    category = models.ManyToManyField(Category, related_name="commands")
    description = models.TextField(max_length=10000, blank=True, null=True)
    example = models.CharField(max_length=2000, blank=True, null=True)
    tooltip = models.CharField(max_length=1000, blank=True, null=True)
    option = models.ManyToManyField(Option, related_name="commands", blank=True)
    alternative = models.ManyToManyField("self", symmetrical=False, related_name="alternative_to", blank=True)
    
    copy_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def increment_copy_count(self):
        self.copy_count += 1
        self.save()
