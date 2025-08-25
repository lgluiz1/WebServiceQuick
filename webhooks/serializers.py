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
  "previsao_entrega": "2025-08-30",
  "observacoes": "Entrega urgente",
  "agente_entrega": "Transportadora XYZ",
  "numero_nfe": "123456789",
  "serie_nfe": "1",
  "chave_nfe": "12345678901234567890123456789012345678901234",
  "data_emissao_nfe": "2025-08-20",
  "id_nfe": "NFE12345",
  "cte_id": "CTE12345",
  "cte_numero": "987654321",
  "cte_key": "CTEKEY1234567890",
  "data_emissao_cte": "2025-08-21",
  "minuta_id": "MIN12345",
  "minuta_numero": "555666",
  "minuta_data_emissao": "2025-08-22",
  "doc_remetente": "12345678901",
  "nome_remetente": "Empresa Remetente",
  "doc_destinatario": "98765432100",
  "nome_destinatario": "João Silva",
  "cidade_destino": "São Paulo",
  "uf_destino": "SP",
  "cep_destino": "01000-000",
  "endereco_destino": "Rua Exemplo, 100",
  "bairro_destino": "Centro",
  "tel_destinatario": "(11) 99999-8888",
  "email_destinatario": "joao.silva@email.com",
  "manifesto_id": "MAN12345",
  "manifesto_numero": "777888",
  "manifesto_data_emissao": "2025-08-23",
  "motorista": "Carlos Pereira",
  "doc_motorista": "12345678900",
  "veiculo_placa": "ABC1D23"
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