from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True) #  SKU (Stock Keeping Unit) - Identificador único del producto

    def __str__(self):
        return self.nombre
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0) #  La cantidad no puede ser negativa
    fecha_actualizacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades - Ubicacion: {self.ubicacion.nombre}'
