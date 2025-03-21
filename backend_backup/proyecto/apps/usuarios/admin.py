from django.contrib import admin
from .models import Usuario, Rol
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

class UsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = ("username", "email", "rol", "nombre", "apellido")

class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "rol", "nombre", "apellido")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def clean_username(self):
        return self.cleaned_data.get("username") or None


class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm  # <-- Usa tu formulario personalizado
    model = Usuario
    list_display = ('email', 'username', 'nombre', 'apellido', 'rol', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellido', 'email', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (  # <-- Usa *tu* configuración, no la de UserAdmin
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre', 'apellido', 'rol', 'password', 'password2'),
        }),
    )

    # Añade esto:
    def save_model(self, request, obj, form, change):
        print("Errores del formulario:", form.errors)  # <-- Imprime los errores
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
