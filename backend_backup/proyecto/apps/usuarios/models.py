from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class Rol(models.Model):
    ROL_CHOICES = (
        ('conductor', 'Conductor'),
        ('cliente', 'Cliente'),
        ('jefe_inventario', 'Jefe de Inventario'),
        ('jefe_empresa', 'Jefe de Empresa'),
	('admin', 'Admin'),
    )
    nombre = models.CharField(max_length=20, choices=ROL_CHOICES, unique=True)

    def __str__(self):
        return self.get_nombre_display() #  o self.nombre, si quieres mostrar el valor interno


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True) # blank=True permite que sea opcional
    apellido = models.CharField(max_length=255, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    def __str__(self):
        return self.email
