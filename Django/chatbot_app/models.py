from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='transacciones')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Transacciones"

    def __str__(self):
        return f"{self.categoria} - {self.monto} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class Presupuesto(models.Model):
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE, related_name='presupuesto')
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return f"{self.categoria} - Límite: {self.limite} - Gastado: {self.gastado}"

from django.utils import timezone

class Ingreso(models.Model):
    fuente = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return f"Ingreso de {self.fuente} - {self.monto} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class InformeMensual(models.Model):
    mes = models.DateField(unique=True)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gastos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Informes Mensuales"

    def actualizar_balance(self):
        self.balance = self.ingresos_totales - self.gastos_totales
        self.save()

    def __str__(self):
        return f"Informe {self.mes.strftime('%Y-%m')} - Balance: {self.balance}"