from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario

@receiver(post_save, sender=Usuario)
def enviar_email_boas_vindas(sender, instance, created, **kwargs):
    if created:  # só envia se for um novo usuário
        assunto = "Bem-vindo ao sistema!"
        mensagem = (
            f"Olá {instance.nome},\n\n"
            "Seu cadastro foi realizado com sucesso no nosso sistema.\n"
            "Agora você pode acessar e aproveitar nossos serviços.\n\n"
            "Atenciosamente,\n"
            "Equipe do Sistema"
        )

        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,  # email remetente
            [instance.email],             # email do usuário cadastrado
            fail_silently=False,
        )
