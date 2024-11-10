from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaccion, Categoria, Ingreso, InformeMensual
from django.db.models import Sum
import requests
import json
from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransaccionSerializer
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaccion, Categoria, Ingreso, InformeMensual, Cuenta
from django.db.models import Sum
import requests
import json
from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TransaccionSerializer, CuentaSerializer
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def index(request):
    # Información de la empresa
    info_empresa = {
        "nombre": "Anibenji",
        "descripcion": "Controla tus ingresos y gastos para una mejor administración financiera.",
    }
    
    # Datos para el gráfico de Gastos por Categoría
    datos_categorias = Transaccion.objects.values('categoria__nombre').annotate(total=Sum('monto'))
    categorias = [item['categoria__nombre'] for item in datos_categorias]
    totales_categorias = [float(item['total']) for item in datos_categorias]

    # Datos para el gráfico de Ingresos y Gastos Mensuales
    ingresos_mensuales = Ingreso.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Sum('monto')).order_by('mes')
    gastos_mensuales = Transaccion.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Sum('monto')).order_by('mes')

    meses = sorted(set([item['mes'] for item in ingresos_mensuales] + [item['mes'] for item in gastos_mensuales]))
    meses_str = [mes.strftime('%Y-%m') for mes in meses]

    ingresos_dict = {item['mes']: float(item['total']) for item in ingresos_mensuales}
    gastos_dict = {item['mes']: float(item['total']) for item in gastos_mensuales}

    ingresos_lista = [ingresos_dict.get(mes, 0) for mes in meses]
    gastos_lista = [gastos_dict.get(mes, 0) for mes in meses]

    # Datos para el gráfico de Balance Mensual
    balances_mensuales = InformeMensual.objects.all().order_by('mes')
    meses_balance = [balance.mes.strftime('%Y-%m') for balance in balances_mensuales]
    balances = [float(balance.balance) for balance in balances_mensuales]

    context = {
        'info_empresa': info_empresa,
        'datos_categorias': json.dumps(categorias),
        'totales_categorias': json.dumps(totales_categorias),
        'meses': json.dumps(meses_str),
        'ingresos_mensuales': json.dumps(ingresos_lista),
        'gastos_mensuales': json.dumps(gastos_lista),
        'meses_balance': json.dumps(meses_balance),
        'balances_mensuales': json.dumps(balances),
    }

    return render(request, 'gestion/index.html', context)

@csrf_exempt
def chat_bot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Configuración de la URL de Rasa
            RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
            
            # Enviar mensaje a Rasa
            rasa_payload = {
                "sender": request.session.get('session_id', 'default_user'),
                "message": user_message
            }
            
            response = requests.post(RASA_API_URL, json=rasa_payload)
            
            if response.status_code == 200:
                bot_responses = response.json()
                messages = [msg.get('text', '') for msg in bot_responses]
                return JsonResponse({
                    'status': 'success',
                    'messages': messages
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Error en la comunicación con el bot'
            }, status=500)
            
        except Exception as e:
            logger.error(f"Error en chat_bot: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

@api_view(['GET', 'POST'])
def create_expense(request):
    if request.method == 'POST':
        logger.info(f"Received data for create_expense: {request.data}")
        serializer = TransaccionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Gasto registrado exitosamente."}, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            logger.error(f"Validation errors in create_expense: {error_messages}")
            return Response({"message": "Error al registrar el gasto.", "errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response({"message": "GET request successful"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_budget(request):
    try:
        total_ingresos = Ingreso.objects.aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = Transaccion.objects.aggregate(total=Sum('monto'))['total'] or 0
        presupuesto_actual = total_ingresos - total_gastos
        return Response({"presupuesto_actual": presupuesto_actual})
    except Exception as e:
        logger.error(f"Error in check_budget: {str(e)}")
        return Response({"error": "Error al obtener el presupuesto"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def generate_report(request):
    try:
        fecha_actual = timezone.now().date()
        fecha_inicio = fecha_actual - relativedelta(months=1)
        
        gastos = Transaccion.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_actual)
        total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0
        
        gastos_por_categoria = gastos.values('categoria__nombre').annotate(total=Sum('monto'))
        
        reporte = {
            "total_gastos": total_gastos,
            "gastos_por_categoria": list(gastos_por_categoria)
        }
        
        return Response({"reporte": reporte})
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return Response({"error": "Error al generar el reporte"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def consultar_saldo(request, numero_cuenta):
    try:
        cuenta = Cuenta.objects.get(numero_cuenta=numero_cuenta)
        return Response({
            "saldo": str(cuenta.saldo),
            "moneda": cuenta.moneda
        })
    except Cuenta.DoesNotExist:
        return Response(
            {"error": "Cuenta no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def consultar_estado_cuenta(request, numero_cuenta):
    try:
        cuenta = Cuenta.objects.get(numero_cuenta=numero_cuenta)
        transacciones = cuenta.transacciones.all().order_by('-fecha')[:10]
        
        data = {
            "numero_cuenta": cuenta.numero_cuenta,
            "saldo_actual": str(cuenta.saldo),
            "moneda": cuenta.moneda,
            "ultimas_transacciones": [
                {
                    "fecha": t.fecha.strftime('%Y-%m-%d %H:%M'),
                    "tipo": t.tipo,
                    "monto": str(t.monto),
                    "descripcion": t.descripcion
                } for t in transacciones
            ]
        }
        return Response(data)
    except Cuenta.DoesNotExist:
        return Response(
            {"error": "Cuenta no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def convertir_moneda(request):
    try:
        monto = float(request.GET.get('monto', 0))
        moneda_origen = request.GET.get('de', 'USD')
        moneda_destino = request.GET.get('a', 'USD')
        
        # Aquí deberías integrar una API de conversión real
        # Este es un ejemplo simplificado
        tasas = {
            'USD': 1.0,
            'EUR': 0.85,
            'MXN': 20.0,
            'PEN': 3.70
        }
        
        if moneda_origen not in tasas or moneda_destino not in tasas:
            return Response(
                {"error": "Moneda no soportada"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultado = monto * (tasas[moneda_destino] / tasas[moneda_origen])
        
        return Response({
            "monto_original": monto,
            "moneda_origen": moneda_origen,
            "monto_convertido": round(resultado, 2),
            "moneda_destino": moneda_destino
        })
    except Exception as e:
        logger.error(f"Error en conversión de moneda: {str(e)}")
        return Response(
            {"error": "Error en la conversión"}, 
            status=status.HTTP_400_BAD_REQUEST
        )