from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
import requests
from django.db import transaction
from .models import ManifestoWebhook
from manifesto.models import Manifesto, ManifestoModelo, Descarregamento, Minuta, ResumoNatureza
from filial.models import Filial
from datetime import datetime


@shared_task(bind=True, max_retries=3, default_retry_delay=60, rate_limit='1/m')
def enviar_manifesto_task(self, manifesto_webhook_id):
    """
    Task para enviar manifesto via API externa com:
    - máximo de 3 tentativas
    - delay de 60s entre retries
    - rate limit de 1 execução por minuto
    """
    try:
        raw = ManifestoWebhook.objects.get(id=manifesto_webhook_id)
        
        # Se já tiver processado com sucesso, não enviar de novo
        if raw.processado:
            return f"Manifesto {raw.manifesto_numero} já processado."
        
        url = "https://eo3fzsd6736qa1q.m.pipedream.net"
        data = {"manifesto_id": raw.payload.get("dados", {}).get("manifesto_id")}
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            raw.processado = True
            raw.processado_em = datetime.now()
            raw.erro = None
            raw.save()
            return f"Manifesto {raw.manifesto_numero} enviado com sucesso."
        else:
            # Caso a resposta não seja 200, incrementa tentativas e tenta novamente
            raise Exception(f"Erro ao enviar: {response.status_code} - {response.text}")
    
    except Exception as e:
        # Incrementa tentativas no banco
        if hasattr(raw, 'tentativas_envio'):
            raw.tentativas_envio += 1
        else:
            raw.tentativas_envio = 1
        raw.erro = str(e)
        raw.save()
        
        # Se ainda não excedeu max_retries, agenda retry com delay
        if raw.tentativas_envio < self.max_retries:
            raise self.retry(exc=e, countdown=self.default_retry_delay)
        
        # Se excedeu tentativas, apenas registra o erro
        return f"Falha ao enviar manifesto {raw.manifesto_numero}: {e}"


@shared_task
def processar_manifesto(id):
    try:
        raw = ManifestoWebhook.objects.get(id=id)
        payload = raw.payload
        dados = payload.get("dados", {})

        with transaction.atomic():
            # --------------------
            # Manifesto principal
            # --------------------
            manifesto, created = Manifesto.objects.get_or_create(
                manifesto_numero=dados.get("manifesto_numero")
            )
            manifesto.manifesto_id = dados.get("manifesto_id")
            manifesto.data_emissao = dados.get("manifesto_data_emissao")
            manifesto.filial_embarque = dados.get("filial_embarque")
            manifesto.autor_documento = dados.get("autor_documento")
            manifesto.filial_origem = dados.get("filial_origem")
            manifesto.filial_destino = dados.get("filial_destino")
            manifesto.estado_origem = dados.get("estado_origem")
            manifesto.estado_destino = dados.get("estado_destino")
            manifesto.cidade_descarregamento = dados.get("cidade_descarregamento")
            manifesto.estado_passagem = dados.get("estado_passagem")
            manifesto.cidade_passagem = dados.get("cidade_passagem")
            manifesto.tipo_do_contrato = dados.get("tipo_do_contrato")
            manifesto.status = dados.get("status")
            manifesto.agente_responsavel = dados.get("agente_responsavel")
            manifesto.tipo_manifesto = dados.get("tipo_manifesto")
            manifesto.qtd_volumes = dados.get("qtd_volumes")
            manifesto.qtd_destinos = dados.get("qtd_destinos")
            manifesto.qtd_notas = dados.get("qtd_notas")
            manifesto.peso_total = dados.get("peso_total")
            manifesto.peso_taxado = dados.get("peso_taxado")
            manifesto.valor_total = dados.get("valor_total")
            manifesto.motorista = dados.get("motorista")
            manifesto.veiculo_placa = dados.get("veiculo_placa")
            manifesto.motorista_cpf = dados.get("motorista_cpf")
            manifesto.motorista_cnh = dados.get("motorista_cnh")
            manifesto.previsao_saida = dados.get("previsao_saida")
            manifesto.previsao_entrega = dados.get("previsao_entrega")
            manifesto.observacoes_operacionais = dados.get("observacoes_operacionais", "")
            manifesto.save()

            # --------------------
            # Modelos
            # --------------------
            for m in dados.get("manifesto_modelo", []):
                modelo = ManifestoModelo.objects.filter(
                    manifesto=manifesto, tipo=m.get("tipo")
                ).first()
                if not modelo:
                    modelo = ManifestoModelo(manifesto=manifesto, tipo=m.get("tipo"))
                modelo.qtd = m.get("qtd")
                modelo.save()

            # --------------------
            # Descarregamentos
            # --------------------
            for d in dados.get("descarregamento_dados", []):
                descarregamento = Descarregamento.objects.filter(
                    manifesto=manifesto,
                    local=d.get("local"),
                    data_hora=d.get("data_hora_descarregamento")
                ).first()
                if not descarregamento:
                    descarregamento = Descarregamento(
                        manifesto=manifesto,
                        local=d.get("local"),
                        data_hora=d.get("data_hora_descarregamento")
                    )
                descarregamento.qtd_volumes = d.get("qtd_volumes_descarregados")
                descarregamento.peso_total = d.get("peso_total_descarregado")
                descarregamento.qtd_notas = d.get("qtd_notas_descarregadas")
                descarregamento.valor_total = d.get("valor_total_descarregado")
                descarregamento.save()

            # --------------------
            # Minutas
            # --------------------
            for m in dados.get("minutas", []):
                minuta = Minuta.objects.filter(
                    manifesto=manifesto,
                    minuta_id=m.get("minuta_id")
                ).first()
                if not minuta:
                    minuta = Minuta(manifesto=manifesto, minuta_id=m.get("minuta_id"))
                minuta.minuta_numero = m.get("minuta_numero")
                minuta.data_emissao = m.get("minuta_data_emissao")
                minuta.save()

            # --------------------
            # Resumo por natureza
            # --------------------
            for r in dados.get("resumo_por_natureza", []):
                resumo = ResumoNatureza.objects.filter(
                    manifesto=manifesto, natureza=r.get("natureza")
                ).first()
                if not resumo:
                    resumo = ResumoNatureza(manifesto=manifesto, natureza=r.get("natureza"))
                resumo.qtd = r.get("qtd")
                resumo.save()

            # --------------------
            # Filiais
            # --------------------
            for f in dados.get("filial_emissao", []):
                filial = Filial.objects.filter(documento=f.get("documento")).first()
                if not filial:
                    filial = Filial(documento=f.get("documento"))
                filial.ie = f.get("ie")
                filial.nome = f.get("nome")
                filial.endereco = f.get("endereco")
                filial.bairro = f.get("bairro")
                filial.cidade = f.get("cidade")
                filial.uf = f.get("uf")
                filial.cep = f.get("cep")
                filial.save()

            # --------------------
            # Marca como processado
            # --------------------
            raw.processado = True
            raw.processado_em = datetime.now()
            raw.save()

            enviar_manifesto_task.delay(raw.id)

        return f"Manifesto {manifesto.manifesto_numero} processado com sucesso."

    except Exception as e:
        raw.erro = str(e)
        raw.save()
        raise


