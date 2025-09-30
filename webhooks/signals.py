from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ManifestoWebhook
from .tasks import processar_manifesto

@receiver(post_save, sender=ManifestoWebhook)
def processar_manifesto_signal(sender, instance, **kwargs):
    processar_manifesto.delay(instance.id)