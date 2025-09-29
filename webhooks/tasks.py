from celery import shared_task
from django.db import transaction
from .models import ManifestoWebhook
from manifesto.models import Manifesto, ManifestoModelo, Descarregamento, Minuta, ResumoNatureza
from datetime import datetime

@shared_task
def processar_manifesto(id):
    try:
        raw = ManifestoWebhook.objects.get(id=id)
        payload = raw.payload
        dados = payload.get("dados", {})

        with transaction.atomic():
            manifesto, created = Manifesto.objects.get_or_create(
                manifesto_numero=dados.get("manifesto_numero"),
                defaults={
                    "manifesto_id": dados.get("manifesto_id"),
                    "data_emissao": dados.get("manifesto_data_emissao"),
                    "filial_embarque": dados.get("filial_embarque"),
                    "autor_documento": dados.get("autor_documento"),
                    "filial_origem": dados.get("filial_origem"),
                    "filial_destino": dados.get("filial_destino"),
                    "estado_origem": dados.get("estado_origem"),
                    "estado_destino": dados.get("estado_destino"),
                    "cidade_descarregamento": dados.get("cidade_descarregamento"),
                    "estado_passagem": dados.get("estado_passagem"),
                    "cidade_passagem": dados.get("cidade_passagem"),
                    "tipo_do_contrato": dados.get("tipo_do_contrato"),
                    "status": dados.get("status"),
                    "agente_responsavel": dados.get("agente_responsavel"),
                    "tipo_manifesto": dados.get("tipo_manifesto"),
                    "qtd_volumes": dados.get("qtd_volumes"),
                    "qtd_destinos": dados.get("qtd_destinos"),
                    "qtd_notas": dados.get("qtd_notas"),
                    "peso_total": dados.get("peso_total"),
                    "peso_taxado": dados.get("peso_taxado"),
                    "valor_total": dados.get("valor_total"),
                    "motorista": dados.get("motorista"),
                    "veiculo_placa": dados.get("veiculo_placa"),
                    "motorista_cpf": dados.get("motorista_cpf"),
                    "motorista_cnh": dados.get("motorista_cnh"),
                    "previsao_saida": dados.get("previsao_saida"),
                    "previsao_entrega": dados.get("previsao_entrega"),
                    "observacoes_operacionais": dados.get("observacoes_operacionais", "")
                }
            )

            # --------------------
            # Modelos
            # --------------------
            for m in dados.get("manifesto_modelo", []):
                ManifestoModelo.objects.create(
                    manifesto=manifesto,
                    tipo=m.get("tipo"),
                    qtd=m.get("qtd")
                )

            # --------------------
            # Descarregamentos
            # --------------------
            for d in dados.get("descarregamento_dados", []):
                dt = d.get("data_hora_descarregamento")
                Descarregamento.objects.create(
                    manifesto=manifesto,
                    local=d.get("local"),
                    data_hora=dt,
                    qtd_volumes=d.get("qtd_volumes_descarregados"),
                    peso_total=d.get("peso_total_descarregado"),
                    qtd_notas=d.get("qtd_notas_descarregadas"),
                    valor_total=d.get("valor_total_descarregado")
                )

            # --------------------
            # Minutas
            # --------------------
            for m in dados.get("minutas", []):
                Minuta.objects.create(
                    manifesto=manifesto,
                    minuta_id=m.get("minuta_id"),
                    minuta_numero=m.get("minuta_numero"),
                    data_emissao=m.get("minuta_data_emissao")
                )

            # --------------------
            # Resumo por natureza
            # --------------------
            for r in dados.get("resumo_por_natureza", []):
                ResumoNatureza.objects.create(
                    manifesto=manifesto,
                    natureza=r.get("natureza"),
                    qtd=r.get("qtd")
                )

            # Marca como processado
            raw.processado = True
            raw.processado_em = datetime.now()
            raw.save()

        return f"Manifesto {manifesto.manifesto_numero} processado com sucesso."

    except Exception as e:
        raw.erro = str(e)
        raw.save()
        raise
