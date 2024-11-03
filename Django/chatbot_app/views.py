# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaccion, Categoria, Ingreso, InformeMensual
from django.db.models import Sum
import requests
import json
from django.db.models.functions import TruncMonth



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
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)