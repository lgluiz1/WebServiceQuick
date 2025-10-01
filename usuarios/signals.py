from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
import threading

@receiver(post_save, sender=Usuario)
def enviar_email_ativacao(sender, instance, **kwargs):
    # se o usuário ainda não tiver token de ativação ou não estiver ativo
    if not hasattr(instance, "token_ativacao") or not instance.ativo:
        token = instance.gerar_token_ativacao()
        link_ativacao = f"{settings.SITE_URL}/ativar-conta/{token}/"

        assunto = "Ative sua conta no sistema"
        mensagem = (
            f"Olá {instance.nome},\n\n"
            f"Seu cadastro foi realizado. Para ativar sua conta, clique no link abaixo:\n"
            f"{link_ativacao}\n\n"
            "Se você não fez esse cadastro, ignore este e-mail."
        )

        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
        
