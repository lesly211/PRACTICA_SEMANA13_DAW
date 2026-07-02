from django.contrib import admin
from .models import LoteForestal


@admin.register(LoteForestal)
class LoteForestalAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'especie', 'estado', 'cantidad_m3', 'responsable', 'fecha_registro']
    list_filter = ['estado', 'especie']
    search_fields = ['codigo', 'especie', 'origen']
