from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Usuario

@receiver(post_save, sender=Usuario)
def enviar_email_boas_vindas(sender, instance, created, **kwargs):
    if created:
        # Gerar token de ativação
        token = get_random_string(48)
        instance.token_ativacao = token
        instance.save(update_fields=["token_ativacao"])

        # Criar link de ativação
        link_ativacao = f"{settings.SITE_URL}/ativar-conta/{token}/"

        # Corpo do email
        assunto = "Ative sua conta no sistema"
        mensagem = (
            f"Olá {instance.nome},\n\n"
            f"Seu cadastro foi realizado com sucesso no nosso sistema.\n"
            f"Para ativar sua conta e definir sua senha, clique no link abaixo:\n"
            f"{link_ativacao}\n\n"
            "Se você não realizou esse cadastro, ignore este e-mail.\n\n"
            "Atenciosamente,\n"
            "Equipe do Sistema"
        )

        # Enviar email
        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
