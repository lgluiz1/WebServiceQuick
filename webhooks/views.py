from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.views import SpectacularAPIView
from django.utils import timezone
from .models import FretesWebhook , NfeWebhook, ManifestoWebhook
from .serializers import FreteWebhookSerializer, NfeSenacWebhookSerializer, ManifestoWebhookSerializer
from .tasks import processar_manifesto


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
                            "chave": 12345678901234567890123456789012345678901234,
                            "numero": 123,
                            "serie": 1,
                            "status": [
                                {
                                    "codigo": 1,
                                    "descricao": "Entregue"
                                },
                                {
                                    "codigo": 2,
                                    "descricao": "Cancelada"
                                },
                                {
                                    "codigo": 3,
                                    "descricao": "Em trânsito"
                                },
                            ],
                            "filial_emissao":[
                            {
                                "documento": 12345678901234,
                                "ie": 123456789,
                                "nome": "Empresa XYZ",
                                "endereco": "Rua Exemplo, 100",
                                "bairro": "Centro",
                                "cidade": "São Paulo",
                                "uf": "SP",
                                "cep": "01000-000",
                                }
                              ],
                            "data_emissao": "2025-08-25T10:30:00Z",
                            "data_saida_entrada": "2025-08-25T12:00:00Z",
                            "tipo_operacao": "fracionado",
                            "modelo_frete": "Rodoviario",
                            "valor_total_produtos": 1500.75,
                            "tipo_servico": "Normal",
                            "tipo_emissao": "nfe, cte, minuta",
                            "valor_total_nota": 1600.50,
                            "peso_total_nota": 25.5,
                            "origem": [
                                {   
                                    "documento": 12345678901234,
                                    "cidade": "São Paulo",
                                    "uf": "SP",
                                    "cep": "01000-000",
                                    "endereco": "Rua Exemplo, 100",
                                    "bairro": "Centro",
                                }
                            ],
                            "destino": [
                                {
                                    "documento": 98765432109876,
                                    "nome": "Empresa Destinatária/Cliente Final",
                                    "cidade": "Rio de Janeiro",
                                    "uf": "RJ",
                                    "cep": "20000-000",
                                    "endereco": "Avenida Exemplo, 200",
                                    "bairro": "Centro",
                                    "complemento": "Sala 101",
                                    "telefone": 11999999999,
                                    "email": "destinatario@email",
                                }
                            ],
                            "notas_fiscais": [
                                {
                                    "chave": "12345678901234567890123456789012345678901234",
                                    "numero": 123,
                                    "serie": 1,
                                },
                             
                            ],
                            "observacoes": "Entrega via transportadora X",
                            "url_comprovante": "https://quickdelivery.com/comprovante/000123.pdf"
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
                defaults={
                    "processado": False,
                    "erro": None,
                    "recebido_em": timezone.now(),
                    "payload": payload
                }
            )
            # dispara task Celery
            from fretes.tasks import processar_frete_task
            processar_frete_task.delay(webhook.id)
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
                "numero_nfe": 123456,
                "dados": {
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
                            
                        ],
                        "ctes": [
                            {
                                "cte_id": "CTE12345",
                                "minuta_id": "MIN12345",
                                "cte_numero": 987654321,
                                "cte_key": "12345678901234567890123456789012345678901234",
                                "data_emissao_cte": "2025-08-21",
                            },
                            
                        ],
                        "filial_emissao": [
                            {
                                "documento": 12345678901234,
                                "ie": 123456789,
                                "nome": "Empresa XYZ",
                                "endereco": "Rua Exemplo, 100",
                                "bairro": "Centro",
                                "cidade": "São Paulo",
                                "uf": "SP",
                                "cep": "01000-000",
                            }
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
        ]  # mantive seus exemplos
    )
    def post(self, request, *args, **kwargs):
        serializer = ManifestoWebhookSerializer(data=request.data)
        if serializer.is_valid():
            try:
                manifesto, created = ManifestoWebhook.objects.update_or_create(
                    manifesto_numero=request.data.get("manifesto_numero"),
                    defaults={
                        "payload": request.data,
                        "processado": False,
                        "processado_em": None,
                        "erro": None,
                    },
                )

                # dispara task Celery
                processar_manifesto.delay(manifesto.id)

                return Response(
                    {
                        "message": "Webhook recebido com sucesso!",
                        "id": manifesto.id,
                        "created": created,
                    },
                    status=200,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=500
                )
        return Response(serializer.errors, status=400)