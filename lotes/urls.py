from rest_framework.routers import DefaultRouter
from .views import LoteForestalViewSet

# FASE 3 - DefaultRouter genera automaticamente todas las rutas del
# ModelViewSet (list, detail, y los @action definidos) y mantiene el
# principio DRY: no se escribe una URLConf manual por cada endpoint.
router = DefaultRouter()
router.register(r'lotes', LoteForestalViewSet, basename='lote')

urlpatterns = router.urls
