from django.contrib import admin
from .models import Usuario, Rol
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.models import Group  

admin.site.register(Usuario)  # Registro simple
admin.site.register(Rol)
