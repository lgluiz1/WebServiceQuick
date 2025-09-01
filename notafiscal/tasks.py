from celery import shared_task, chain
from .functions import processar_dados_senac , obter_dados_notas_fiscais
from webhooks.models import NfeWebhook
from .models import NotaFiscal , IntegracaoSenac
from integracoes.functions import enviar_email
from datetime import datetime
import time


@shared_task
def buscar_dados_task():
    print("Buscando dados...")
    import time
    time.sleep(10)  # simula processamento pesado

    hoje_dia = datetime.now()
    hoje_str = hoje_dia.strftime("%Y%m%d")
    
    dados = obter_dados_notas_fiscais()  # roda dentro da task

    NfeWebhook.objects.create(
        numero_nfe=hoje_str,
        recebido_em=hoje_dia,
        processado=False,
        erro=None,
        payload=dados
    )
    # Data do buscar
    titulo_email = f"Busca de notas fiscais DataExport ESL {hoje_dia.strftime('%d/%m/%Y')}"
    email_mensagem = f"Busca de notas fiscais DataExport ESL concluida com sucesso."
    enviar_email(titulo_email, email_mensagem) 

    return "Dados buscados com sucesso!"


@shared_task
def processar_notas_task():
    nfe_webhooks = NfeWebhook.objects.filter(processado=False)
    novas_notas_fiscais = 0
    notas_repetidas = 0

    for nfe_webhook in nfe_webhooks:
        payload_list = nfe_webhook.payload  # lista de dicionários

        for item in payload_list:
            id_nota_fiscal = item.get("ice_f_e_ioe_number")
            chave_nfe = item.get("ice_f_e_ioe_key")

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

                time.sleep(2)

        nfe_webhook.processado = True
        nfe_webhook.save()

    titulo_email = "Processamento Notas Senac"
    email_mensagem = f"✅ Processado {novas_notas_fiscais} notas fiscais. {notas_repetidas} notas fiscais repetidas."
    enviar_email(titulo_email, email_mensagem)    

    return {
        "novas_notas_fiscais": novas_notas_fiscais,
        "notas_repetidas": notas_repetidas
    }

@shared_task
def processar_notas_senac_task():
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
                    time.sleep(1)
                else:
                    notas_repetidas += 1
                    print(f"🔁 Nota fiscal {id_nota_fiscal} ({cnpj_emitente}) já existe, ignorada.")
                    # 2 segundos de espera
                    time.sleep(1)
                

        # Marca NfeWebhook como processado
        nfe_webhook.processado = True
        nfe_webhook.save()

    titulo_email = "Envio Feito para senac"
    email_mensagem = f"✅ Processado {novas_notas_fiscais} notas fiscais. {notas_repetidas} notas fiscais repetidas."
    enviar_email(titulo_email, email_mensagem)

    return {
        "novas_notas_fiscais": novas_notas_fiscais,
        "notas_repetidas": notas_repetidas
    }

# Função que encadeia as duas tasks
@shared_task
def buscar_e_processar_wrapper():
    # Importa as tasks individuais
    from .tasks import buscar_dados_task, processar_notas_senac_task

    # Roda a primeira task e espera o resultado
    result = buscar_dados_task.apply()  # apply() roda de forma síncrona, garante que termine
    print("Buscar dados finalizado:", result.result)

    # Depois roda a segunda task
    result2 = processar_notas_senac_task.apply()
    print("Processar dados finalizado:", result2.result)

    return "Busca e Processamento finalizados!"