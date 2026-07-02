import django_filters
from .models import LoteForestal


class LoteForestalFilter(django_filters.FilterSet):
    """
    FASE 4 - Filtrado por query params sobre campos frecuentes.
    Ejemplos de uso:
      /api/lotes/?estado=verificado
      /api/lotes/?especie=Cedro&cantidad_min=5
    """
    especie = django_filters.CharFilter(field_name='especie', lookup_expr='icontains')
    cantidad_min = django_filters.NumberFilter(field_name='cantidad_m3', lookup_expr='gte')
    cantidad_max = django_filters.NumberFilter(field_name='cantidad_m3', lookup_expr='lte')

    class Meta:
        model = LoteForestal
        fields = ['estado', 'especie', 'origen']
