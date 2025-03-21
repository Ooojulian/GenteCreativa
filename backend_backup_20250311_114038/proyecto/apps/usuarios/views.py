from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsOwner, IsConductor  # Importa los permisos
from .models import Usuario, Rol  # Importa los modelos
from .serializers import UsuarioSerializer, RolSerializer  # Importa los serializadores
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]  # Cualquiera puede crear (registrarse)
        elif self.action == 'list':
            permission_classes = [IsAdminUser]  # Solo admins listan usuarios
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsOwner] # Admin o el propio usuario
        else:
            permission_classes = [IsAuthenticated] # El resto, autenticado
        return [permission() for permission in permission_classes]

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class RefreshTokenView(TokenRefreshView):
    permission_classes = (IsAuthenticated,)
