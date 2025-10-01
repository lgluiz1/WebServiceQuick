# app/tasks.py
from celery import shared_task
from filial.models import Filial
from fretes.models import Frete
from notafiscal.models import NotaFiscal
from webhooks.models import FretesWebhook
from datetime import datetime

def get_or_create_filial(data):
    """Verifica se a filial já existe, senão cria"""
    documento = str(data.get("documento"))
    filial, created = Filial.objects.update_or_create(
        documento=documento,
        defaults={
            "ie": data.get("ie"),
            "nome": data.get("nome", "Não informado"),
            "endereco": data.get("endereco"),
            "bairro": data.get("bairro"),
            "cidade": data.get("cidade"),
            "uf": data.get("uf"),
            "cep": data.get("cep"),
        }
    )
    return filial

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def processar_frete_task(self, json_data):
    try:
        # Se vier no formato antigo (com 'dados'), use ele
        dados = json_data.get("dados", json_data)  
        frete_id = json_data.get("frete_id", dados.get("frete_id"))

        # Resto do processamento...
        # Filiais
        filial_emissao = get_or_create_filial(dados["filial_emissao"][0])
        origem = get_or_create_filial(dados["origem"][0])
        destino = get_or_create_filial(dados["destino"][0])

        # Frete
        frete, created = Frete.objects.update_or_create(
            frete_id=frete_id,
            defaults={
                "chave": dados["chave"],
                "numero": dados["numero"],
                "serie": dados["serie"],
                "status": dados["status"][0]["codigo"] if isinstance(dados["status"], list) else dados["status"],
                "filial_emissao": filial_emissao,
                "origem": origem,
                "destino": destino,
                "data_emissao": dados["data_emissao"],
                "data_saida_entrada": dados["data_saida_entrada"],
                "tipo_operacao": dados["tipo_operacao"],
                "modelo_frete": dados["modelo_frete"],
                "valor_total_produtos": dados["valor_total_produtos"],
                "tipo_servico": dados["tipo_servico"],
                "tipo_emissao": dados["tipo_emissao"],
                "valor_total_nota": dados["valor_total_nota"],
                "peso_total_nota": dados["peso_total_nota"],
                "observacoes": dados.get("observacoes"),
                "url_comprovante": dados.get("url_comprovante"),
            }
        )

        # Notas fiscais
        for nf in dados.get("notas_fiscais", []):
            NotaFiscal.objects.update_or_create(
                chave=nf["chave"],
                defaults={
                    "frete": frete,
                    "numero": nf["numero"],
                    "serie": nf["serie"],
                }
            )

        # Atualiza webhook
        if "frete_id" in json_data:
            FretesWebhook.objects.filter(frete_id=frete.frete_id).update(
                processado=True,
                processado_em=datetime.now(),
                erro=None,
            )

        return f"Frete {frete.frete_id} processado com sucesso."

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
