from django.utils import timezone
from django.db import models
from category.models import Category, SubCategory


class Routine(models.Model):
    active = models.BooleanField(default=False)
    routine = models.CharField(max_length=30000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="routine")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="routine", blank=True, null=True)
    example = models.CharField(max_length=2000, blank=True, null=True)
    tooltip = models.CharField(max_length=1000, blank=True, null=True)
    
    creation_date = models.DateTimeField(default=timezone.now)
    creator_name = models.CharField(max_length=255, blank=True, null=True)
    creator_email = models.CharField(max_length=255, blank=True, null=True)
    creator_message = models.CharField(max_length=10000, blank=True, null=True)

    copy_count = models.IntegerField(default=0)

    def __str__(self):
        return self.command
    
    def increment_copy_count(self):
        self.copy_count += 1
        self.save()