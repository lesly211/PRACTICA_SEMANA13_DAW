from rest_framework import serializers
from .models import LoteForestal


class LoteForestalSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer principal con estilo HATEOAS: cada recurso incluye su propia
    URL ('url') para que el cliente pueda navegar la API sin depender de
    documentacion externa (uniform interface).
    """

    # FASE 2 - campo de solo lectura calculado, no existe como columna en BD
    responsable_nombre = serializers.SerializerMethodField()
    # PrimaryKeyRelatedField: no hay endpoint de usuarios expuesto en esta
    # practica, por eso el responsable se referencia por id (no por hyperlink)
    responsable = serializers.PrimaryKeyRelatedField(read_only=True)

    # FASE 2 - ReadOnlyField: expone el label legible del choice sin permitir
    # que el cliente lo sobrescriba directamente
    estado_display = serializers.ReadOnlyField(source='get_estado_display')

    class Meta:
        model = LoteForestal
        # FASE 2 - lista explicita de campos: nunca se usa '__all__' para no
        # exponer accidentalmente campos sensibles como 'costo_interno'
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
        """
        Validacion anidada / cruzada entre campos (no se puede validar en un
        solo campo): un lote 'verificado' no puede tener cantidad menor a 1 m3
        (regla de negocio del area de control de calidad).
        """
        estado = data.get('estado', getattr(self.instance, 'estado', None))
        cantidad = data.get('cantidad_m3', getattr(self.instance, 'cantidad_m3', None))
        if estado == LoteForestal.Estado.VERIFICADO and cantidad is not None and cantidad < 1:
            raise serializers.ValidationError(
                {'estado': 'Un lote no puede marcarse como verificado con menos de 1 m3.'}
            )
        return data


class LoteForestalSimpleSerializer(serializers.ModelSerializer):
    """
    Version ligera (no hipervinculada) usada en el endpoint de reporte
    (@action) donde no se requiere navegacion HATEOAS completa.
    """
    class Meta:
        model = LoteForestal
        fields = ['id', 'codigo', 'especie', 'estado', 'cantidad_m3']
