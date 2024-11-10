from rest_framework import serializers
from .models import Transaccion, Categoria
from django.utils.dateparse import parse_date
from rest_framework import serializers
from .models import Cuenta, Transaccion

class TransaccionSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    fecha = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y'])

    class Meta:
        model = Transaccion
        fields = ['id', 'categoria', 'monto', 'descripcion', 'fecha']

    def validate_fecha(self, value):
        if isinstance(value, str):
            try:
                return parse_date(value)
            except ValueError:
                raise serializers.ValidationError("Formato de fecha inválido. Use YYYY-MM-DD.")
        return value

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['numero_cuenta', 'saldo', 'moneda']

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'fecha', 'descripcion']