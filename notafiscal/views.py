from django.http import JsonResponse
from .functions import obter_dados_notas_fiscais
from webhooks.models import NfeWebhook
from .models import IntegracaoSenac
from datetime import datetime

def buscar_dados(request):
    hoje_dia = datetime.now()
    hoje_str = hoje_dia.strftime("%Y%m%d")

    dados = obter_dados_notas_fiscais()

    # Cria um objeto NfeWebhook para cada dado encontrado
    
    NfeWebhook.objects.create(
        numero_nfe=hoje_str,
        recebido_em=hoje_dia,
        processado=False,
        erro=None,
        payload=dados
        )

    # Retorna os dados como JSON
    return JsonResponse(dados, safe=False)

def processar_dados_senac(request):
    # Pega registros NfeWebhook com status False
    nfe_webhooks = NfeWebhook.objects.filter(processado=False)
    

    for nfe_webhook in nfe_webhooks:
        payload_list = nfe_webhook.payload  # lista de dicionários

        # Itera sobre cada item na lista
        for item in payload_list:
            id_nota_fiscal = item.get("ice_f_e_ioe_number")
            if id_nota_fiscal:
                # Evita duplicidade: cria só se não existir
                criado = IntegracaoSenac.objects.get_or_create(
                    id_nota_fiscal=id_nota_fiscal,
                    defaults={
                        "status": False,
                        "dados": item
                    }
                )
                
            # Se já existia, apenas ignora
            if criado:
                print(f"Nota fiscal {id_nota_fiscal} criada.")
            else:
                print(f"Nota fiscal {id_nota_fiscal} já existe, ignorada.")

        # Marca NfeWebhook como processado
        nfe_webhook.processado = True
        nfe_webhook.save()

    return JsonResponse({"message": "Dados processados com sucesso!"})