from django.utils import timezone
from django.db import models

class Category(models.Model):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=10000, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=10000, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.title