from celery import shared_task
from time import sleep
from notafiscal.models import IntegracaoSenac
from .functions import envia_para_senac_soap  # sua função já existente

@shared_task
def integracao_senac_task():
    integracoes = IntegracaoSenac.objects.filter(status=False)

    if not integracoes.exists():
        return {"message": "Nenhuma integração encontrada.", "integracoes_processadas": 0, "falhas": []}

    sucesso = 0
    falhas = []

    for integracao in integracoes:
        try:
            # Envia os dados para o SOAP do Senac
            status_code, resposta = envia_para_senac_soap(integracao.dados)

            if status_code == 200:
                integracao.status = True
                integracao.erro = None
                integracao.save()
                sucesso += 1
            else:
                integracao.erro = f"Falha no envio: {status_code} - {resposta}"
                integracao.save()
                falhas.append({
                    "id": integracao.id,
                    "status_code": status_code,
                    "resposta": resposta
                })

            sleep(5)  # mantém o delay entre envios

        except Exception as e:
            integracao.erro = f"Exceção: {str(e)}"
            integracao.save()
            falhas.append({
                "id": integracao.id,
                "erro": str(e)
            })

    return {
        "message": "Processamento concluído.",
        "integracoes_processadas": sucesso,
        "falhas": falhas
    }
