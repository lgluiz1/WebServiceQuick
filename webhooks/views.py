from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.views import SpectacularAPIView
from django.utils import timezone
from .models import FretesWebhook , NfeWebhook, ManifestoWebhook
from .serializers import FreteWebhookSerializer, NfeSenacWebhookSerializer, ManifestoWebhookSerializer


class ReceberWebhookAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FreteWebhookSerializer,
        responses={200: FreteWebhookSerializer},
        examples=[
        OpenApiExample(
            'Exemplo de webhook',
            value={
                "frete_id": "FRT12345",
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
                            "tel_destinatario": "11999998888",
                            "email_destinatario": "joao.silva@email.com",
                            "manifesto_id": "MAN12345",
                            "manifesto_numero": "777888",
                            "manifesto_data_emissao": "2025-08-23",
                            "motorista": "Carlos Pereira",
                            "doc_motorista": "12345678900",
                            "veiculo_placa": "ABC1D23"
                        }

            },
            request_only=True,  # indica que é exemplo para envio
        )
    ]
)
    
    def post(self, request):
        serializer = FreteWebhookSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            frete_id = data.get("frete_id")
            payload = data.get("dados", data)  # se "dados" existir, use, senão salva tudo
            webhook, created = FretesWebhook.objects.update_or_create(
                frete_id=frete_id,
                processado=False,
                erro=None,
                defaults={
                    "recebido_em": timezone.now(),
                    "payload": payload
                }
            )
            return Response({
                "status": "ok",
                "frete_id": webhook.frete_id,
                "recebido_em": webhook.recebido_em.isoformat()
            })
        return Response(serializer.errors, status=400)

class ReceberWebhookNfeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FreteWebhookSerializer,
        responses={200: FreteWebhookSerializer},
        examples=[
        OpenApiExample(
            'Exemplo de webhook',
            value={
                "frete_id": "FRT12345",
                "dados": {
                            "chave": "12345678901234567890123456789012345678901234",
                            "numero": "000123",
                            "serie": "1",
                            "status": "Finalizada , Cancelada, Em_transporte",
                            "data_emissao": "2025-08-25T10:30:00Z",
                            "data_saida_entrada": "2025-08-25T12:00:00Z",
                            "tipo_operacao": "saída",
                            "valor_total_produtos": "1500.75",
                            "valor_total_nota": "1600.50",
                            "peso_total_nota": "25.5",
                            "observacoes": "Entrega via transportadora X",
                            "nome_emitente": "Empresa Emitente LTDA",
                            "documento_emitente": "12.345.678/0001-90",
                            "nome_destinatario": "João da Silva",
                            "documento_destinatario": "123.456.789-00",
                            "endereco_destinatario": "Rua das Flores, 123",
                            "bairro_destinatario": "Centro",
                            "cidade_destinatario": "São Paulo",
                            "uf_destinatario": "SP",
                            "cep_destinatario": "01000-000",
                            "telefone_destinatario": "11999999999",
                            "email_destinatario": "joao.silva@quickdelivery.com.br",
                            "url_comprovante": "https://quickdelivery.com/comprovante/000123.pdf"
                        }

                        },
                        request_only=True,  # indica que é exemplo para envio
                        )
                    ]
                )

    def post(self, request):
        serializer = NfeSenacWebhookSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            numero_nfe = data.get("numero_nfe")
            payload = data.get("dados", data)  # se "dados" existir, use, senão salva tudo
            webhook, created = NfeWebhook.objects.update_or_create(
                numero_nfe=numero_nfe,
                processado=False,
                erro=None,
                defaults={
                    "recebido_em": timezone.now(),
                    "payload": payload
                }
            )
            return Response({
                "status": "ok",
                "numero_nfe": webhook.numero_nfe,
                "recebido_em": webhook.recebido_em.isoformat()
            })
        return Response(serializer.errors, status=400)
    
class ReceberWebhookManifestoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ManifestoWebhookSerializer,
        responses={200: ManifestoWebhookSerializer},
        examples=[
            OpenApiExample(
                "Exemplo de webhook",
                value={
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
                            {"tipo": "transferencia", "qtd": 10},
                            {"tipo": "coleta", "qtd": 5},
                        ],
                        "qtd_volumes": 10,
                        "qtd_destinos": 5,
                        "qtd_notas": 15,
                        "peso_total": 1500.75,
                        "peso_taxado": 1600.00,
                        "valor_total": 25000.50,
                        "descarregamento_dados": [
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
                            },
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
                            },
                        ],
                        "ctes": [
                            {
                                "cte_id": "CTE12345",
                                "cte_numero": 987654321,
                                "cte_key": "12345678901234567890123456789012345678901234",
                                "data_emissao_cte": "2025-08-21",
                            },
                            {
                                "cte_id": "CTE67890",
                                "cte_numero": 123456789,
                                "cte_key": "43210987654321098765432109876543210987654321",
                                "data_emissao_cte": "2025-08-20",
                            },
                        ],
                        "notas": [
                            {
                                "numero_nota": 123456789,
                                "serie_nota": 1,
                                "chave_nota": "12345678901234567890123456789012345678901234",
                                "data_emissao_nota": "2025-08-20",
                            },
                            {
                                "numero_nota": 987654321,
                                "serie_nota": 2,
                                "chave_nota": "43210987654321098765432109876543210987654321",
                                "data_emissao_nota": "2025-08-19",
                            },
                        ],
                        "motorista": "Carlos Souza",
                        "veiculo_placa": "ABC-1234",
                        "motorista_cpf": "12345678901",
                        "motorista_cnh": "12345678901",
                        "previsao_saida": "2025-08-25T12:00:00Z",
                        "previsao_entrega": "2025-08-30",
                        "observacoes_operacionais": "",
                        "resumo_por_natureza": [
                            {"natureza": "natureza 1", "qtd": 5},
                            {"natureza": "natureza 2", "qtd": 10},
                        ],
                    },
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = ManifestoWebhookSerializer(data=request.data)
        if serializer.is_valid():
            try:
                manifesto = ManifestoWebhook.objects.create(
                    manifesto_numero=request.data.get("manifesto_numero"),
                    payload=request.data,
                )
                return Response(
                    {"message": "Webhook recebido com sucesso!", "id": manifesto.id},
                    status=200,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=500
                )
        return Response(serializer.errors, status=400)