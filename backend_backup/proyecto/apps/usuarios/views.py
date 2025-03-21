from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from .permissions import IsOwner, IsConductor
from .models import Usuario, Rol
from .serializers import UsuarioSerializer, RolSerializer


# Vistas de DRF para JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Clase de permiso personalizada para verificar si el usuario es el propietario del objeto
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Comprueba si el usuario autenticado es el propietario del objeto
        return obj == request.user

class UsuarioViewSet(viewsets.ModelViewSet): #Aquí estaba el error
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]  # Cualquiera puede crear usuarios (registro)
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsOwner]  # Solo admins pueden listar usuarios
        else:
            permission_classes = [IsAuthenticated]  # Resto de acciones, requiere autenticación
        return [permission() for permission in permission_classes]

    # Para el login (obtener token) - Usa la vista de djangorestframework-simplejwt
class LoginView(TokenObtainPairView):
   permission_classes = (AllowAny,) #Permitir a todos, ya que es el login

class RefreshTokenView(TokenRefreshView):
    permission_classes = (IsAuthenticated,) #Solo usuarios autenticados pueden refrescar.


# Permiso para rol de conductor

class IsConductor(BasePermission):
    message = "No tienes permiso para acceder a esta vista, no eres un conductor." #Mensaje de error
    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado y tiene el rol de 'conductor'.
        return request.user.is_authenticated and request.user.rol.nombre == 'conductor'
