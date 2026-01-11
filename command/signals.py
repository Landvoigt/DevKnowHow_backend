from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Command


@receiver(post_save, sender=Command)
def sync_alternatives(sender, instance, created, **kwargs):
    for alt in instance.alternative.all():
        if instance.pk not in alt.alternative.values_list('pk', flat=True):
            alt.alternative.add(instance)
