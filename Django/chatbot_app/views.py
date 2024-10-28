from django.shortcuts import render
from .models import Transaccion, Categoria, Ingreso, InformeMensual
from django.db.models import Sum

def index(request):
    # Información de la empresa
    info_empresa = {
        "nombre": "Tienda de Ropa XYZ",
        "descripcion": "Controla tus ingresos y gastos para una mejor administración financiera.",
    }

    # Datos para el gráfico de gastos por categoría
    datos_categorias = Transaccion.objects.values('categoria__nombre').annotate(total=Sum('monto'))

    # Datos para ingresos y gastos mensuales
    ingresos_mensuales = Ingreso.objects.values('fecha__month').annotate(total=Sum('monto')).order_by('fecha__month')
    gastos_mensuales = Transaccion.objects.values('fecha__month').annotate(total=Sum('monto')).order_by('fecha__month')

    # Balance mensual
    balances_mensuales = InformeMensual.objects.all().order_by('mes')

    return render(request, 'gestion/index.html', {
        'info_empresa': info_empresa,
        'datos_categorias': datos_categorias,
        'ingresos_mensuales': ingresos_mensuales,
        'gastos_mensuales': gastos_mensuales,
        'balances_mensuales': balances_mensuales,
    })
