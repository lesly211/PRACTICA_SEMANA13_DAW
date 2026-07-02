from rest_framework.routers import DefaultRouter
from .views import LoteForestalViewSet

router = DefaultRouter()
router.register(r'lotes', LoteForestalViewSet, basename='lote')

urlpatterns = router.urls
