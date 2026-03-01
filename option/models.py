from django.db import models

from command.models import Command


class Option(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="option")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    level = models.IntegerField(default=0)
    combinable = models.BooleanField(default=True)
    standalone = models.BooleanField(default=False)
    value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ("command", "title")

    def __str__(self):
        return self.title
    