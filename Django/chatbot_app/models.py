from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Transaccion(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria} - {self.monto} - {self.fecha}"

class Presupuesto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.categoria} - Limite: {self.limite} - Gastado: {self.gastado}"

class Ingreso(models.Model):
    fuente = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Ingreso de {self.fuente} - {self.monto} - {self.fecha}"

class InformeMensual(models.Model):
    mes = models.CharField(max_length=20)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gastos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def actualizar_balance(self):
        self.balance = self.ingresos_totales - self.gastos_totales
        self.save()

    def __str__(self):
        return f"Informe {self.mes} - Balance: {self.balance}"
