from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from category.models import Category
from tag.models import Tag


class Command(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=2000)
    description = models.TextField(max_length=10000, blank=True, null=True)
    context = models.CharField(max_length=50, blank=True, null=True)
    context_description = models.CharField(max_length=2000, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="commands")
    example = ArrayField(models.CharField(max_length=2000), blank=True, default=list)
    tooltip = models.CharField(max_length=1000, blank=True, null=True)
    alternative = models.ManyToManyField("self", symmetrical=True, related_name="alternative_to", blank=True)
    equivalent = models.ManyToManyField("self", symmetrical=True, related_name="equivalent_to", blank=True)
    tag = models.ManyToManyField(Tag, blank=True, related_name="commands")
    
    copy_count = models.IntegerField(default=0)

    """ 
    Run this SQL command in your PostgreSQL database to enable the pg_trgm extension for trigram indexing:
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    """
    class Meta:
        indexes = [
            models.Index(fields=["active"]),
            
            GinIndex(
                fields=["title"],
                name="cmd_title_trgm",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["description"],
                name="cmd_desc_trgm",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.title
        