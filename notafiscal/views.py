from django.http import JsonResponse
from .functions import obter_dados_notas_fiscais, processar_dados_senac
from webhooks.models import NfeWebhook
from .models import IntegracaoSenac
from datetime import datetime
from django.http import JsonResponse
from time import sleep
from integracoes.functions import envia_para_senac_soap
from .tasks import buscar_dados_task

def buscar_dados(request):
    task = buscar_dados_task.delay()  # dispara async
    return JsonResponse({
        "status": "task enviada",
        "task_id": task.id
    })

def processar_notas_senac(request):
    nfe_webhooks = NfeWebhook.objects.filter(processado=False)
    novas_notas_fiscais = 0
    notas_repetidas = 0
    lista_cnpj_senac = ["03709814004002"]  # CNPJs permitidos

    for nfe_webhook in nfe_webhooks:
        payload_list = nfe_webhook.payload  # lista de dicionários

        for item in payload_list:
            id_nota_fiscal = item.get("ice_f_e_ioe_number")
            chave_nfe = item.get("ice_f_e_ioe_key")
            cnpj_emitente = item.get("ice_f_e_ioe_iur_document")  # <- campo do CNPJ

            # Só processa se o CNPJ estiver na lista
            if cnpj_emitente not in lista_cnpj_senac:
                print(f"⏭️ Nota {id_nota_fiscal} ignorada (CNPJ {cnpj_emitente} não é do Senac).")
                continue

            # Garante que chave_nfe não seja vazio/nulo
            if not chave_nfe:
                print(f"⚠️ Nota fiscal {id_nota_fiscal} sem chave_nfe, ignorada.")
                continue

            if id_nota_fiscal:
                obj, created = IntegracaoSenac.objects.get_or_create(
                    chave_nfe=chave_nfe,
                    defaults={
                        "id_nota_fiscal": id_nota_fiscal,
                        "status": False,
                        "dados": item
                    }
                )

                if created:
                    novas_notas_fiscais += 1
                    print(f"✅ Nota fiscal {id_nota_fiscal} ({cnpj_emitente}) criada com chave {chave_nfe}.")
                else:
                    notas_repetidas += 1
                    print(f"🔁 Nota fiscal {id_nota_fiscal} ({cnpj_emitente}) já existe, ignorada.")

                # 2 segundos de espera
                sleep(2)

        # Marca NfeWebhook como processado
        nfe_webhook.processado = True
        nfe_webhook.save()

    return JsonResponse({
        "message": f"Dados processados com sucesso! Novas notas fiscais: {novas_notas_fiscais}, notas repetidas: {notas_repetidas}"
    }, status=200)


def envio_unico_chave_senac(request, chave_nfe):
    # Busca a nota pela chave
    obj = IntegracaoSenac.objects.filter(chave_nfe=chave_nfe).first()

    if not obj:
        return JsonResponse(
            {"status_code": 404, "resposta": "Chave NFE não encontrada"},
            status=404
        )

    dados = obj.dados  # só acessa depois de garantir que obj existe

    # Aqui você precisa de uma função que processe apenas 1 nota
    status_code, resposta = envia_para_senac_soap(dados)

    # Muda Status para True se envio bem-sucedido
    if status_code == 200:
        obj.status = True
        obj.save()

    # Muda Status para False se envio falhar
    else:
        obj.status = False
        obj.save()

    return JsonResponse(
        {"status_code": status_code, "resposta": resposta},
        status=status_code
    )