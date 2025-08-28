from django.shortcuts import render
from notafiscal.models import IntegracaoSenac
from .functions import envia_para_senac_soap
from django.http import JsonResponse
from time import sleep

def integracao_senac(request):
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
                # ✅ sucesso → marca como processada e zera o erro
                integracao.status = True
                integracao.erro = None
                integracao.save()
                sucesso += 1
            else:
                # ❌ falha → mantém status=False e salva erro
                integracao.erro = f"Falha no envio: {status_code} - {resposta}"
                integracao.save()
                falhas.append({
                    "id": integracao.id,
                    "status_code": status_code,
                    "resposta": resposta
                })

            sleep(5)

        except Exception as e:
            # ❌ erro inesperado
            integracao.erro = f"Exceção: {str(e)}"
            integracao.save()
            falhas.append({
                "id": integracao.id,
                "erro": str(e)
            })

    return JsonResponse({
        "message": "Processamento concluído.",
        "integracoes_processadas": sucesso,
        "falhas": falhas
    })