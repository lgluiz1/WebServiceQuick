from django.core.mail import send_mail
from django.conf import settings

def dispara_email(usuario_email , mensagem , assunto):
    assunto = "Processo concluído com sucesso ✅"
    mensagem = "Olá, seu processo foi finalizado com sucesso!"
    remetente = settings.DEFAULT_FROM_EMAIL  # configurado no settings.py
    destinatarios = [usuario_email]

    send_mail(assunto, mensagem, remetente, destinatarios)
