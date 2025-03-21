from django.contrib import admin
from .models import Producto, Ubicacion, Inventario

admin.site.register(Producto)
admin.site.register(Ubicacion)
admin.site.register(Inventario)
