from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    MONEDA_CHOICES = [
        ('USD', 'Dólares'),
        ('EUR', 'Euros'),
        ('PEN', 'Soles'),
        ('MXN', 'Pesos Mexicanos')
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    numero_cuenta = models.CharField(max_length=20, unique=True, verbose_name="Número de cuenta")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo")
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='USD', verbose_name="Moneda")
    
    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - {self.usuario.username}"

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('DEPOSITO', 'Depósito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CONVERSION', 'Conversión de Moneda')  # Nuevo tipo
    ]
    
    cuenta = models.ForeignKey(
        Cuenta, 
        on_delete=models.CASCADE, 
        related_name='transacciones',
        verbose_name="Cuenta"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='transacciones',
        verbose_name="Categoría"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Fecha")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    
    # Nuevos campos para conversión de moneda
    moneda_origen = models.CharField(max_length=3, null=True, blank=True, verbose_name="Moneda Origen")
    moneda_destino = models.CharField(max_length=3, null=True, blank=True, verbose_name="Moneda Destino")
    tasa_conversion = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        null=True, 
        blank=True, 
        verbose_name="Tasa de Conversión"
    )

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.categoria} - {self.monto} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class Presupuesto(models.Model):
    categoria = models.OneToOneField(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='presupuesto',
        verbose_name="Categoría"
    )
    limite = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Límite")
    gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Gastado")

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return f"{self.categoria} - Límite: {self.limite} - Gastado: {self.gastado}"

class Ingreso(models.Model):
    cuenta = models.ForeignKey(
        Cuenta, 
        on_delete=models.CASCADE, 
        related_name='ingresos',
        verbose_name="Cuenta",
        null=True,  # Temporalmente permitimos null
        blank=True
    )
    fuente = models.CharField(max_length=100, verbose_name="Fuente")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Fecha")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Ingreso de {self.fuente} - {self.monto} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class InformeMensual(models.Model):
    cuenta = models.ForeignKey(
        Cuenta, 
        on_delete=models.CASCADE, 
        related_name='informes',
        verbose_name="Cuenta",
        null=True,
        blank=True
    )
    mes = models.DateField(unique=True, verbose_name="Mes")
    ingresos_totales = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Ingresos totales"
    )
    gastos_totales = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Gastos totales"
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Balance"
    )

    class Meta:
        verbose_name = "Informe Mensual"
        verbose_name_plural = "Informes Mensuales"
        ordering = ['-mes']
        
    def actualizar_balance(self):
        self.balance = self.ingresos_totales - self.gastos_totales
        self.save()

    def __str__(self):
        return f"Informe {self.mes.strftime('%Y-%m')} - Balance: {self.balance}"
