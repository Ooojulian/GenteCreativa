from django.db import models
from apps.usuarios.models import Usuario

class PedidoTransporte(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_cliente')
    conductor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_conductor')
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True) #  Opcional
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    # Otros campos relevantes para el transporte

    def __str__(self):
        return f'Pedido de {self.origen} a {self.destino} ({self.estado})'
