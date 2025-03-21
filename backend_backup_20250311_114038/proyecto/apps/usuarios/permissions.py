from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios de un objeto editarlo.
    """
    message = "No tienes permiso para acceder a este objeto, no eres el propietario." #Mensaje de error
    def has_object_permission(self, request, view, obj):
        # La propiedad 'user' se establece automáticamente en las vistas de DRF
        return obj == request.user

#class IsConductor(permissions.BasePermission):
 #   message = "No tienes permiso para acceder a esta vista, no eres un conductor." #Mensaje de error
  #  def has_permission(self, request, view):
   #     # Verifica si el usuario está autenticado y tiene el rol de 'conductor'.
    #    return request.user.is_authenticated and request.user.rol.nombre == 'conductor'

class IsConductor(permissions.BasePermission):
    message = "No tienes permiso para acceder a esta vista, no eres un conductor."

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado.
        if not request.user.is_authenticated:
            return False  # Si no está autenticado, no hay permiso

        # Verifica si el usuario tiene un rol asignado *antes* de acceder a .nombre
        if request.user.rol is None:
            return False  # Si no tiene rol, no es conductor

        return request.user.rol.nombre == 'conductor'
