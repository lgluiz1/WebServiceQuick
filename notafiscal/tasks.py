from celery import shared_task
from .functions import processar_dados_senac

@shared_task
def processar_nfe_task():
    processar_dados_senac()

    return "Processamento concluido"
