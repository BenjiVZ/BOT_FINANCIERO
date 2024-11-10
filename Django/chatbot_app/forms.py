from django import forms
from .models import Cuenta, Transaccion

class ConversionMonedaForm(forms.Form):
    cuenta_origen = forms.ModelChoiceField(
        queryset=Cuenta.objects.all(),
        label='Cuenta Origen',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    monto = forms.DecimalField(
        label='Monto a convertir',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    moneda_destino = forms.ChoiceField(
        choices=Cuenta.MONEDA_CHOICES,
        label='Moneda Destino',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ConsultaSaldoForm(forms.Form):
    cuenta = forms.ModelChoiceField(
        queryset=Cuenta.objects.all(),
        label='Seleccione la cuenta',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ConsultaEstadoCuentaForm(forms.Form):
    cuenta = forms.ModelChoiceField(
        queryset=Cuenta.objects.all(),
        label='Seleccione la cuenta',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateField(
        label='Fecha Inicio',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    fecha_fin = forms.DateField(
        label='Fecha Fin',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

class HistorialTransaccionesForm(forms.Form):
    cuenta = forms.ModelChoiceField(
        queryset=Cuenta.objects.all(),
        label='Seleccione la cuenta',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_transaccion = forms.ChoiceField(
        choices=[('', 'Todas')] + list(Transaccion.TIPO_CHOICES),
        required=False,
        label='Tipo de Transacción',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateField(
        label='Desde',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    fecha_fin = forms.DateField(
        label='Hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    ) 