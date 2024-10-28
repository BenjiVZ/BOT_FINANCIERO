from django.contrib import admin

# Register your models here.
from .models import Categoria, Transaccion, Presupuesto

admin.site.register(Categoria)
admin.site.register(Transaccion)
admin.site.register(Presupuesto)
