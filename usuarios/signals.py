from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario

@receiver(post_save, sender=Usuario)
def enviar_email_ativacao(sender, instance, **kwargs):
    def send_activation_email(sender, instance, created):

        if created :
            send_mail(
                'Bem-vindo ao Sistema',
                f'Seu usuário foi criado com sucesso. Seu email de login é: {instance.email}',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )

