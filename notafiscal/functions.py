import requests
import time
from datetime import datetime, timedelta
from .models import IntegracaoSenac
from webhooks.models import NfeWebhook

def obter_dados_notas_fiscais():
    hoje = datetime.now()
    ontem = hoje - timedelta(days=1)

    data_inicio = ontem.strftime("%Y-%m-%d")
    data_fim = hoje.strftime("%Y-%m-%d")

    template_id = 8856
    empresa = "quickdelivery"
    token = "zyUq31Mq6gMcYGzV4zL7HTsdnS7pULjaQoxGbkPZ1cLDoxT3d-Xukw"

    url = f"https://{empresa}.eslcloud.com.br/api/analytics/reports/{template_id}/data"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    todos_dados = []
    pagina = 1
    per_page = 100

    while True:
        payload = {
            "search": {
                "invoice_occurrences": {
                    "occurrence_at": f"{data_inicio} - {data_fim}",
                    "trigger": "finish"
                }
            },
            "page": pagina,
            "per": per_page
        }

        response = requests.get(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()

            if not data or len(data) == 0:
                break

            todos_dados.extend(data)
            time.sleep(2)
            pagina += 1

        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
            break

    return todos_dados

# função processa Json recebido em nfeWebhook e cria um objeto integraçãoSenac para cada item do Json
def processar_dados_senac():
    nfe_webhooks = NfeWebhook.objects.filter(processado=False)
    novas_notas_fiscais = 0
    notas_repetidas = 0

    for nfe_webhook in nfe_webhooks:
        payload_list = nfe_webhook.payload  # lista de dicionários

        for item in payload_list:
            id_nota_fiscal = item.get("ice_f_e_ioe_number")
            chave_nfe = item.get("ice_f_e_ioe_key")

            # Garante que chave_nfe não seja vazio/nulo
            if not chave_nfe:
                print(f"⚠️ Nota fiscal {id_nota_fiscal} sem chave_nfe, ignorada.")
                continue

            if id_nota_fiscal:
                obj, created = IntegracaoSenac.objects.get_or_create(
                    chave_nfe=chave_nfe,
                    defaults={
                        "status": False,
                        "dados": item
                    }
                )

                if created:
                    novas_notas_fiscais += 1
                    print(f"✅ Nota fiscal {id_nota_fiscal} com chave {chave_nfe} criada.")
                else:
                    notas_repetidas += 1
                    print(f"🔁 Nota fiscal {id_nota_fiscal} com chave {chave_nfe} já existe, ignorada.")

                # 2 segundos de espera
                time.sleep(2)

        # Marca NfeWebhook como processado
        nfe_webhook.processado = True
        nfe_webhook.save()

    return {
        "novas_notas_fiscais": novas_notas_fiscais,
        "notas_repetidas": notas_repetidas
    }
