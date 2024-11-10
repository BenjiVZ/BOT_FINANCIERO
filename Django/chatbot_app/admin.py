from django.contrib import admin
from .models import Categoria, Transaccion, Presupuesto, Cuenta, Ingreso, InformeMensual

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'categoria', 'monto', 'fecha', 'cuenta')
    list_filter = ('tipo', 'categoria', 'fecha')
    search_fields = ('descripcion', 'cuenta__numero_cuenta')
    date_hierarchy = 'fecha'

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta', 'usuario', 'saldo', 'moneda')
    search_fields = ('numero_cuenta', 'usuario__username')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'limite', 'gastado')
    search_fields = ('categoria__nombre',)

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('fuente', 'monto', 'fecha', 'cuenta')
    list_filter = ('cuenta', 'fecha')
    search_fields = ('fuente', 'descripcion')
    date_hierarchy = 'fecha'

@admin.register(InformeMensual)
class InformeMensualAdmin(admin.ModelAdmin):
    list_display = ('mes', 'cuenta', 'ingresos_totales', 'gastos_totales', 'balance')
    list_filter = ('cuenta', 'mes')
    date_hierarchy = 'mes'