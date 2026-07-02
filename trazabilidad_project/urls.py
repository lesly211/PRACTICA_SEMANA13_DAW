from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # FASE 3 - API (incluye rutas generadas por el DefaultRouter)
    path('api/', include('lotes.urls')),
    path('api-auth/', include('rest_framework.urls')),  # login/logout navegable

    # FASE 5 - Documentacion OpenAPI/Swagger automatica (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
