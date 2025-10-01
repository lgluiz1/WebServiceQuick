# fretes/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Frete
from .tasks import processar_frete_task  # importando a task

@receiver(post_save, sender=Frete)
def enviar_frete_para_processamento(sender, instance, created, **kwargs):
    """
    Dispara a task quando um Frete é criado ou atualizado.
    """
    # Aqui você pode decidir se quer rodar só no create ou também no update
    json_data = {
        "frete_id": instance.frete_id,
        "dados": {
            "chave": instance.chave,
            "numero": instance.numero,
            "serie": instance.serie,
            "status": {"codigo": instance.status},
            "filial_emissao": [{
                "documento": instance.filial_emissao.documento,
                "ie": instance.filial_emissao.ie,
                "nome": instance.filial_emissao.nome,
                "endereco": instance.filial_emissao.endereco,
                "bairro": instance.filial_emissao.bairro,
                "cidade": instance.filial_emissao.cidade,
                "uf": instance.filial_emissao.uf,
                "cep": instance.filial_emissao.cep,
            }],
            "origem": [{
                "documento": instance.origem.documento,
                "ie": instance.origem.ie,
                "nome": instance.origem.nome,
                "endereco": instance.origem.endereco,
                "bairro": instance.origem.bairro,
                "cidade": instance.origem.cidade,
                "uf": instance.origem.uf,
                "cep": instance.origem.cep,
            }],
            "destino": [{
                "documento": instance.destino.documento,
                "ie": instance.destino.ie,
                "nome": instance.destino.nome,
                "endereco": instance.destino.endereco,
                "bairro": instance.destino.bairro,
                "cidade": instance.destino.cidade,
                "uf": instance.destino.uf,
                "cep": instance.destino.cep,
            }],
            "data_emissao": str(instance.data_emissao),
            "data_saida_entrada": str(instance.data_saida_entrada),
            "tipo_operacao": instance.tipo_operacao,
            "modelo_frete": instance.modelo_frete,
            "valor_total_produtos": float(instance.valor_total_produtos),
            "tipo_servico": instance.tipo_servico,
            "tipo_emissao": instance.tipo_emissao,
            "valor_total_nota": float(instance.valor_total_nota),
            "peso_total_nota": float(instance.peso_total_nota),
            "observacoes": instance.observacoes,
            "url_comprovante": instance.url_comprovante,
            "notas_fiscais": [
                {
                    "chave": nf.chave,
                    "numero": nf.numero,
                    "serie": nf.serie,
                } for nf in instance.notafiscal_set.all()
            ]
        }
    }

    # Dispara a task de forma assíncrona
    processar_frete_task.delay(json_data)
