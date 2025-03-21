from django.contrib import admin
from .models import Usuario, Rol
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

# Formulario para *editar* usuarios existentes.
class UsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):  # Hereda de la Meta de UserChangeForm
        model = Usuario
        fields = ("username", "email", "rol", "nombre", "apellido", "cedula")  # Campos para editar

# Formulario para *crear* usuarios.  ¡Aquí está la clave!
class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # <-- ¡IMPORTANTE! Hereda de UserCreationForm.Meta
        model = Usuario
        # *SOLO* los campos que NO son password.  UserCreationForm.Meta ya maneja password.
        fields = ("email", "username", "nombre", "apellido", "rol", "cedula")

    def clean_username(self):
      username = self.cleaned_data.get('username')
      #Si se esta creando, no hay instancia.
      if self.instance.pk is None: #Nuevo usuario
        if Usuario.objects.filter(username = username).exists():
          raise forms.ValidationError("Este nombre de usuario ya existe")
      else: #Edicion de usuario
        if Usuario.objects.filter(username=username).exclude(id = self.instance.pk).exists():
          raise forms.ValidationError("Este nombre de usuario ya existe")

      return username or None

# Clase para administrar Usuarios en el admin de Django.
class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm        # Formulario para editar
    add_form = UsuarioCreationForm  # Formulario para CREAR  <-- ¡Usa el formulario correcto!
    model = Usuario
    list_display = ('cedula', 'email', 'username', 'nombre', 'apellido', 'rol', 'is_staff')

    # Configura cómo se muestran los campos al *editar* un usuario existente.
    fieldsets = (
        (None, {'fields': ('cedula', 'username', 'password')}),  # Incluye password aquí
        ('Información Personal', {'fields': ('nombre', 'apellido', 'email', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Configura cómo se muestran los campos al *CREAR* un nuevo usuario.
    add_fieldsets = UserAdmin.add_fieldsets + (  # <-- ¡IMPORTANTE!  Usa el + para AÑADIR
        ("Campos adicionales", {
            'classes': ('wide',),
            # *NO* incluyas password aquí.  UserCreationForm ya se encarga de eso.
            'fields': ('cedula', 'email', 'username', 'nombre', 'apellido', 'rol'),
        }),
    )
    ordering = ('cedula',)

# Registra los modelos en el admin.
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)