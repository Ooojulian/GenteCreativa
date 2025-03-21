from django.urls import path
from .views import PedidosConductorList, IniciarFinalizarPedido

urlpatterns = [
    path('mis_pedidos/', PedidosConductorList.as_view(), name='mis-pedidos'),
    path('pedidos/<int:pk>/', IniciarFinalizarPedido.as_view(), name='iniciar-finalizar-pedido'),
]
