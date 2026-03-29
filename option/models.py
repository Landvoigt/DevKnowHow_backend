from django.db import models
from django.forms import ValidationError

from command.models import Command
from category.models import Category


class Option(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="option")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    level = models.IntegerField(default=0)
    combinable = models.BooleanField(default=True)
    standalone = models.BooleanField(default=False)
    overwrite = models.BooleanField(default=False)

    class Meta:
        unique_together = ("command", "title")

    def __str__(self):
        return self.title
    
    def clean(self):
        super().clean()

        if self.command:
            valid_categories = self.command.category.all()

            if self.pk:
                selected_categories = self.category.all()

                for cat in selected_categories:
                    if cat not in valid_categories:
                        raise ValidationError(f"Category '{cat}' is not allowed for this command")