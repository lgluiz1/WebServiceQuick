import requests
import time
from datetime import datetime, timedelta

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
