# apps/webhooks/serializers.py
from rest_framework import serializers

class FreteWebhookSerializer(serializers.Serializer):
    frete_id = serializers.CharField()
    dados = serializers.JSONField()

    class Meta:
        swagger_schema_fields = {
            "example": {
                "frete_id": "12345",
                "dados": {
  "frete_id": "FRT12345",
  "recebido_em": "2025-08-25T12:00:00Z",
  "tipo_frete": "Rodoviário",
  "tipo_do_servico": "Coleta",
  "previsao_entrega": "2025-08-30",
  "observacoes": "Entrega urgente",
  "agente_entrega": "Transportadora XYZ",
  "numero_nfe": 123456789,
  "natureza_da_mercadoria": "medicamento-termoalabel",
  "tipo_operacao": "LTL ou FTL",
  "qtd_volumes": 10,
  "peso_real": 1500.75,
  "serie_nfe": 1,
  "chave_nfe": 12345678901234567890123456789012345678901234,
  "data_emissao_nfe": "2025-08-20",
  "id_nfe": "NFE12345",
  "cte_id": "CTE12345",
  "cte_numero": 987654321,
  "cte_key": 12345678901234567890123456789012345678901234,
  "data_emissao_cte": "2025-08-21",
  "minuta_id": "MIN12345",
  "minuta_numero": 555666,
  "minuta_data_emissao": "2025-08-22",
  "doc_remetente": 12345678901,
  "nome_remetente": "Empresa Remetente",
  "doc_destinatario": 98765432100,
  "nome_destinatario": "João Silva",
  "cidade_destino": "São Paulo",
  "uf_destino": "SP",
  "cep_destino": "01000-000",
  "endereco_destino": "Rua Exemplo, 100",
  "bairro_destino": "Centro",
  "tel_destinatario": "(11) 99999-8888",
  "email_destinatario": "joao.silva@email.com",
  "manifesto_id": "MAN12345",
  "manifesto_numero": 777888,
  "manifesto_data_emissao": "2025-08-23",
  "tipo_veiculo": "Truck",
  "trans_redespacho": "Transportadora XYZ",
  "agente_coleta": "Agente Coleta ABC",
  "agente_entrega": "Transportadora XYZ",
}

            }
        }


class NfeSenacWebhookSerializer(serializers.Serializer):
    frete_id = serializers.CharField()
    dados = serializers.JSONField()

    class Meta:
        swagger_schema_fields = {
            "example": {
                "numero_nfe": "12345",
                "dados": {}
            }
        }


class ManifestoWebhookSerializer(serializers.Serializer):
    manifesto_numero = serializers.CharField()
    dados = serializers.JSONField()

    class Meta:
        swagger_schema_fields = {
            "example": {
                "manifesto_numero": 777888,
                "dados": {
    "manifesto_id": "12345",
    "manifesto_numero": 777888,
    "manifesto_data_emissao": "2025-08-23",
    "filial_embarque": "Empresa XYZ",
    "autor_documento": "autor do manifesto",
    "filial_origem": "Filial A",
    "filial_destino": "Filial B",
    "estado_origem": "SP",
    "estado_destino": "RJ",
    "cidade_descarregamento": "duque de caxias",
    "estado_passagem": "MG",
    "cidade_passagem": "belo horizonte",
    "tipo_do_contrato": "proprio",
    "status": "em-transito",
    "agente_responsavel": "Transportadora XYZ",
    "tipo_manifesto": "carga_fracionada",
    
    "manifesto_modelo": [
        {"tipo": "transferencia",
         "qtd": 10
         },
        {"tipo": "coleta",
         "qtd": 5
         },
    ],

    "qtd_volumes": 10,
    "qtd_destinos": 5,
    "qtd_notas": 15,
    "peso_total": 1500.75,
    "peso_taxado": 1600.00,
    "valor_total": 25000.50,

    "descarregamento_dados":[
        {
            "local": "quicklogistics",
            "data_hora_descarregamento": "2025-08-26T15:30:00Z",
            "qtd_volumes_descarregados": 68,
            "peso_total_descarregado": 750.25,
            "qtd_notas_descarregadas": 5,
            "valor_total_descarregado": 12500.25,            
            },
        {
            "local": "cliente final",
            "data_hora_descarregamento": "2025-08-27T10:45:00Z",
            "qtd_volumes_descarregados": 32,
            "peso_total_descarregado": 500.50,
            "qtd_notas_descarregadas": 3,
            "valor_total_descarregado": 7500.75,            
            }
    ],

    "minutas": [
        {
            "minuta_id": "MIN12345",
            "minuta_numero": 555666,
            "minuta_data_emissao": "2025-08-22",
        },
        {
            "minuta_id": "MIN67890",
            "minuta_numero": 777888,
            "minuta_data_emissao": "2025-08-24",
        }
    ],

    "ctes": [
        {
            "cte_id": "CTE12345",
            "cte_numero": 987654321,
            "cte_key": 12345678901234567890123456789012345678901234,
            "data_emissao_cte": "2025-08-21",
        },
        {
            "cte_id": "CTE67890",
            "cte_numero": 123456789,
            "cte_key": 43210987654321098765432109876543210987654321,
            "data_emissao_cte": "2025-08-20",
        }
    ],

    "notas": [
        {
            "numero_nota": 123456789,
            "serie_nota": 1,
            "chave_nota": 12345678901234567890123456789012345678901234,
            "data_emissao_nota": "2025-08-20",
        },
        {
            "numero_nota": 987654321,
            "serie_nota": 2,
            "chave_nota": 43210987654321098765432109876543210987654321,
            "data_emissao_nota": "2025-08-19",
        }
    ],

    "motorista": "Carlos Souza",
    "veiculo_placa": "ABC-1234",
    "motorista_cpf": 12345678901,
    "motorista_cnh": 12345678901,
    "previsao_saida": "2025-08-25T12:00:00Z",
    "previsao_entrega": "2025-08-30",
    "observacoes_operacionais": "", 

    "resumo_por_natureza":[
        {
            "natureza": "natureza 1",
            "qtd": 5
        },
        {
            "natureza": "natureza 2",
            "qtd": 10
        }
    ],
}
            }
        }