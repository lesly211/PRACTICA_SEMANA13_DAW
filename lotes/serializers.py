from rest_framework import serializers
from .models import LoteForestal


class LoteForestalSerializer(serializers.HyperlinkedModelSerializer):
    responsable_nombre = serializers.SerializerMethodField()
    responsable = serializers.PrimaryKeyRelatedField(read_only=True)
    estado_display = serializers.ReadOnlyField(source='get_estado_display')

    class Meta:
        model = LoteForestal
        # exponer accidentalmente campos sensibles como 'costo_interno' IA
        fields = [
            'url', 'id', 'codigo', 'especie', 'origen', 'cantidad_m3',
            'estado', 'estado_display', 'responsable', 'responsable_nombre',
            'fecha_registro', 'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_registro', 'fecha_actualizacion']
        extra_kwargs = {
            'url': {'view_name': 'lote-detail'},
        }

    def get_responsable_nombre(self, obj):
        return obj.responsable.username if obj.responsable else 'Sin asignar'

    def validate_cantidad_m3(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'La cantidad en m3 debe ser mayor que cero.'
            )
        return value

    def validate(self, data):
    
        estado = data.get('estado', getattr(self.instance, 'estado', None))
        cantidad = data.get('cantidad_m3', getattr(self.instance, 'cantidad_m3', None))
        if estado == LoteForestal.Estado.VERIFICADO and cantidad is not None and cantidad < 1:
            raise serializers.ValidationError(
                {'estado': 'Un lote no puede marcarse como verificado con menos de 1 m3.'}
            )
        return data


class LoteForestalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteForestal
        fields = ['id', 'codigo', 'especie', 'estado', 'cantidad_m3']
