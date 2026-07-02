from django.db import models
from django.contrib.auth.models import User


class LoteForestal(models.Model):

    class Estado(models.TextChoices):
        REGISTRADO = 'registrado', 'Registrado'
        EN_TRANSITO = 'en_transito', 'En tránsito'
        VERIFICADO = 'verificado', 'Verificado'
        RECHAZADO = 'rechazado', 'Rechazado'

    codigo = models.CharField(max_length=20, unique=True)
    especie = models.CharField(max_length=100)
    origen = models.CharField(max_length=150, help_text='Zona / concesion forestal de origen')
    cantidad_m3 = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.REGISTRADO)
    responsable = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='lotes_registrados'
    )
    costo_interno = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.codigo} - {self.especie}'
