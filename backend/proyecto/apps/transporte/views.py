from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone # <-- Importa esto
from .models import PedidoTransporte
from .serializers import PedidoTransporteSerializer
from apps.usuarios.permissions import IsConductor  # Importa el permiso


class PedidosConductorList(generics.ListAPIView):
    serializer_class = PedidoTransporteSerializer
    permission_classes = [IsAuthenticated, IsConductor]  # Solo conductores autenticados

    def get_queryset(self):
        # Filtra los pedidos para mostrar solo los asignados al conductor actual.
        return PedidoTransporte.objects.filter(conductor=self.request.user)


class IniciarFinalizarPedido(generics.UpdateAPIView):
    queryset = PedidoTransporte.objects.all()
    serializer_class = PedidoTransporteSerializer
    permission_classes = [IsAuthenticated, IsConductor]

    def get_object(self):
        #Asegura que el conductor solo pueda acceder a sus propios pedidos
        pedido = super().get_object()
        if pedido.conductor != self.request.user:
            return Response({'error': 'No tienes permiso para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)
        return pedido

    def patch(self, request, *args, **kwargs):
        pedido = self.get_object()

        if 'iniciar' in request.data:
            if pedido.estado != 'pendiente':
                return Response({'error': 'El pedido no esta en estado pendiente'}, status=status.HTTP_400_BAD_REQUEST)

            # Información para mostrar ANTES de aceptar (puedes personalizar esto)
            confirmacion = {
                'id': pedido.id,
                'origen': pedido.origen,
                'destino': pedido.destino,
                'descripcion': pedido.descripcion,
                'estado': pedido.estado,
                'confirmar': 'Si, confirmo que deseo iniciar el pedido' #Mensaje agregado
            }

            if request.data.get('iniciar') == 'confirmado':
                 # El conductor ha confirmado, actualiza el estado y la fecha
                pedido.estado = 'en_curso'
                pedido.fecha_inicio = timezone.now()  # Usa timezone.now() para la hora actual
                pedido.save()
                serializer = self.get_serializer(pedido)
                return Response(serializer.data, status=status.HTTP_200_OK) #Devuelve el pedido actualizado.
            else:
               #Mostrar la información de confirmación
               return Response(confirmacion, status=status.HTTP_200_OK)


        elif 'finalizar' in request.data:
            if pedido.estado != 'en_curso':
                return Response({'error': 'El pedido no esta en curso'}, status=status.HTTP_400_BAD_REQUEST)

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
                pedido.fecha_fin = timezone.now()  # Usa timezone.now()
                pedido.save()
                serializer = self.get_serializer(pedido)
                return Response(serializer.data, status=status.HTTP_200_OK) #Devuelve el pedido actualizado
            else:
                #Mostrar la información de confirmación
                return Response(confirmacion, status=status.HTTP_200_OK)

        return Response({'error': 'Debes especificar "iniciar" o "finalizar" en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

    #Para usar el put, se debe enviar un body con todos los datos.
    # def update(self, request, *args, **kwargs):
    #     return Response({'error': 'No se permite la actualización completa'}, status=s
