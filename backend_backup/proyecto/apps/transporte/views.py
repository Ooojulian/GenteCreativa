from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PedidoTransporte
from .serializers import PedidoTransporteSerializer
from apps.usuarios.permissions import IsConductor
from django.utils import timezone

class PedidosConductorList(generics.ListAPIView):
    serializer_class = PedidoTransporteSerializer
    permission_classes = [IsAuthenticated, IsConductor]

    def get_queryset(self):
        return PedidoTransporte.objects.filter(conductor=self.request.user)

class IniciarFinalizarPedido(generics.RetrieveUpdateAPIView):  # Cambiamos a RetrieveUpdateAPIView
    queryset = PedidoTransporte.objects.all()
    serializer_class = PedidoTransporteSerializer
    permission_classes = [IsAuthenticated, IsConductor]

    def get_object(self):
        #Asegura que el conductor solo pueda acceder a sus propios pedidos
        pedido = super().get_object()
        if pedido.conductor != self.request.user:
            raise exceptions.PermissionDenied(
                "No tienes permiso para acceder a este pedido."
            )
        return pedido


    def patch(self, request, *args, **kwargs):
        pedido = self.get_object()

        if 'iniciar' in request.data:
            if pedido.estado != 'pendiente':
                return Response({'error': 'El pedido no está en estado pendiente'}, status=status.HTTP_400_BAD_REQUEST)

            # Información para mostrar ANTES de aceptar (puedes personalizar esto)
            confirmacion = {
                'id': pedido.id,
                'origen': pedido.origen,
                'destino': pedido.destino,
                'descripcion': pedido.descripcion,
                'tipo_vehiculo': "Camión",  # O obtén esto de otro modelo si es necesario
                'tipo_envio': "Carga completa",  # O de otro modelo/campo
                'producto': pedido.cliente.nombre,
                'cliente': pedido.cliente.email,  # O el campo que quieras mostrar
                'estado': pedido.estado,
                'confirmar': 'Si, confirmo que deseo iniciar el pedido' #Mensaje agregado
            }

            if request.data.get('iniciar') == 'confirmado':
                # El conductor ha confirmado, actualiza el estado y la fecha
                pedido.estado = 'en_curso'
                pedido.fecha_inicio = timezone.now()
                pedido.save()
                serializer = self.get_serializer(pedido)
                return Response(serializer.data, status=status.HTTP_200_OK) #Devuelve el pedido actualizado.
            else:
                #Mostrar la información de confirmación
                return Response(confirmacion, status=status.HTTP_200_OK)


        elif 'finalizar' in request.data:
            if pedido.estado != 'en_curso':
                return Response({'error': 'El pedido no está en curso'}, status=status.HTTP_400_BAD_REQUEST)

             # Información para mostrar ANTES de aceptar
            confirmacion = {
                'id': pedido.id,
                'origen': pedido.origen,
                'destino': pedido.destino,
                'estado': pedido.estado,
                'confirmar': 'Si, confirmo que deseo finalizar el pedido' #Mensaje agregado
            }

            if request.data.get('finalizar') == 'confirmado':
                pedido.estado = 'finalizado'
                pedido.fecha_fin = timezone.now()
                pedido.save()
                serializer = self.get_serializer(pedido)
                return Response(serializer.data, status=status.HTTP_200_OK) #Devuelve el pedido actualizado
            else:
                #Mostrar la información de confirmación
                return Response(confirmacion, status=status.HTTP_200_OK)

        return Response({'error': 'Debes especificar "iniciar" o "finalizar" en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)
