from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Webponto
from datetime import datetime

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def webponto(request):
    # Converte a string para objeto datetime
    hora_str = data["hora"]
    dt = datetime.strptime(hora_str, "%Y-%m-%d %H:%M:%S")

    # Separa data e hora
    data = dt.date().isoformat()  # '2025-08-15'
    hora = dt.time().isoformat()  # '07:58:36'

    id_funcionario = request.data.get('id')
    data = request.data.get('data')
    hora = request.data.get('hora')
    nome = request.data.get('nome')
    # Adiciona informaçoes ao banco dados

    

    webponto = Webponto.objects.create(id_funcionario=id_funcionario, data=data, hora=hora, nome=nome)

    return Response({
        "id": webponto.id,
        "data": webponto.data,
        "hora": webponto.hora,
        "nome": webponto.nome
    })
