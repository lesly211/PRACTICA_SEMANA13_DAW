from rest_framework.throttling import SimpleRateThrottle


class ReporteRateThrottle(SimpleRateThrottle):
    """
    FASE 4 - Throttle especifico y mas estricto para el endpoint de reporte
    (@action 'resumen'), que es mas costoso de calcular que un list() normal.
    La tasa 'reporte' se define en settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].
    """
    scope = 'reporte'

    def get_cache_key(self, request, view):
        # Identifica por usuario autenticado o por IP si es anonimo
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {'scope': self.scope, 'ident': ident}
