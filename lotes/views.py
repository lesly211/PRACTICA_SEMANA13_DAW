from django.db.models import Sum, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import LoteForestal
from .serializers import LoteForestalSerializer, LoteForestalSimpleSerializer
from .filters import LoteForestalFilter
from .throttles import ReporteRateThrottle


class LoteForestalViewSet(viewsets.ModelViewSet):
    queryset = LoteForestal.objects.all()
    serializer_class = LoteForestalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LoteForestalFilter
    search_fields = ['codigo', 'especie', 'origen']
    ordering_fields = ['fecha_registro', 'cantidad_m3', 'estado']
    ordering = ['-fecha_registro']

    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=False, methods=['get'], throttle_classes=[ReporteRateThrottle])
    def resumen(self, request):
        datos = (
            LoteForestal.objects
            .values('estado')
            .annotate(total_lotes=Count('id'), total_m3=Sum('cantidad_m3'))
            .order_by('estado')
        )
        return Response({'resumen_por_estado': list(datos)})

    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        lote = self.get_object()
        lote.estado = LoteForestal.Estado.VERIFICADO
        lote.save(update_fields=['estado', 'fecha_actualizacion'])
        serializer = self.get_serializer(lote)
        return Response(serializer.data)
