from django.shortcuts import render
from notafiscal.models import IntegracaoSenac
from .functions import envia_para_senac_soap
from django.http import JsonResponse
from time import sleep

def integracao_senac(request):
    # Buscar todas as integrações que ainda não foram processadas
    integracoes = IntegracaoSenac.objects.filter(status=False)

    if not integracoes.exists():
        return JsonResponse({"message": "Nenhuma integração encontrada."}, status=404)

    sucesso = 0
    falhas = []

    for integracao in integracoes:
        try:
            # Envia os dados para o SOAP do Senac
            status_code, resposta = envia_para_senac_soap(integracao.dados)

            if status_code == 200:
                # Marca como processada se envio for bem-sucedido
                integracao.status = True
                integracao.save()
                sucesso += 1
                sleep(5)
            else:
                # Caso o envio falhe, adiciona na lista de falhas
                falhas.append({
                    "id": integracao.id,
                    "status_code": status_code,
                    "resposta": resposta
                })
                sleep(5)

        except Exception as e:
            falhas.append({
                "id": integracao.id,
                "erro": str(e)
            })

    return JsonResponse({
        "message": "Processamento concluído.",
        "integracoes_processadas": sucesso,
        "falhas": falhas
    })