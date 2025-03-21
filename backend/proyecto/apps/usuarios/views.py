from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsOwner, IsConductor  # Importa los permisos
from .models import Usuario, Rol  # Importa los modelos
from .serializers import UsuarioSerializer, RolSerializer  # Importa los serializadores
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate


#Para crear usuarios y listar usuarios
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
            permission_classes = [IsAuthenticated]  # Resto de acciones, requiere autenticación
        return [permission() for permission in permission_classes]

    # Para el login (obtener token) - Vista Personalizada.
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class RefreshTokenView(TokenRefreshView):
    permission_classes = (IsAuthenticated,)

class ConductorLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        cedula = request.data.get('cedula')

        if not cedula:
            return Response({'error': 'La cédula es obligatoria'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(cedula=cedula, rol__nombre='conductor')
        except Usuario.DoesNotExist:
            return Response({'error': 'Cédula no válida o no eres un conductor'}, status=status.HTTP_401_UNAUTHORIZED)

        # Autenticar al usuario (sin contraseña)
        user = authenticate(request, cedula=cedula)

        if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

class ClienteLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        cedula = request.data.get('cedula')
        if not cedula:
            return Response({'error': 'La cédula es obligatoria'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(cedula=cedula, rol__nombre='cliente')
        except Usuario.DoesNotExist:
            return Response({'error': 'Cédula no válida o no eres un cliente'}, status=status.HTTP_401_UNAUTHORIZED)

        # Autenticar al usuario (sin contraseña)
        user = authenticate(request, cedula=cedula)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            })

        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)