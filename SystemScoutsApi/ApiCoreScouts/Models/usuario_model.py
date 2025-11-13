from django.db import models
from .mantenedor_model import *
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(BaseUserManager):
    def create_user(self, USU_USERNAME, password=None, **extra_fields):
        if not USU_USERNAME:
            raise ValueError('El usuario debe tener un nombre de usuario (USU_USERNAME)')
        usuario = self.model(USU_USERNAME=USU_USERNAME, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, USU_USERNAME, password=None, **extra_fields):
        from .usuario_model import Perfil  # 👈 evita import circular

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('USU_VIGENTE', True)

        if 'PEL_ID' not in extra_fields or extra_fields['PEL_ID'] is None:
            perfil_admin, _ = Perfil.objects.get_or_create(PEL_DESCRIPCION='Administrador', defaults={'PEL_VIGENTE': True})
            extra_fields['PEL_ID'] = perfil_admin

        return self.create_user(USU_USERNAME, password, **extra_fields)

    def get_by_natural_key(self, USU_USERNAME):
        return self.get(USU_USERNAME=USU_USERNAME)

class Usuario(AbstractBaseUser, PermissionsMixin):
    USU_ID = models.BigAutoField(primary_key=True, db_column='USU_ID')
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False, db_column='PEL_ID')
    USU_USERNAME = models.CharField(max_length=100, unique=True, null=False, db_column='USU_USERNAME')
    USU_PASSWORD = models.CharField(max_length=128, null=False, db_column='USU_PASSWORD')
    USU_RUTA_FOTO = models.CharField(max_length=255, null=False, db_column='USU_RUTA_FOTO')
    USU_VIGENTE = models.BooleanField(default=True, null=False, db_column='USU_VIGENTE')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'USU_USERNAME'
    REQUIRED_FIELDS = []

    @property
    def is_active(self):
        return self.USU_VIGENTE
    
    @property
    def id(self):
        return self.USU_ID


    # Django espera estas propiedades
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, raw_password):
        self.USU_PASSWORD = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.USU_PASSWORD)

    class Meta:
        db_table = 'USUARIO'

class Perfil(models.Model):
    PEL_ID = models.BigAutoField(primary_key=True, db_column='PEL_ID')
    PEL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='PEL_DESCRIPCION')
    PEL_VIGENTE = models.BooleanField(default=True, null=False, db_column='PEL_VIGENTE')

    class Meta:
        db_table = 'PERFIL'

class Perfil_Aplicacion(models.Model):
    PEA_ID = models.BigAutoField(primary_key=True, db_column='PEA_ID')
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False, db_column='PEL_ID')
    APL_ID = models.ForeignKey('Aplicacion',on_delete=models.PROTECT, null=False, db_column='APL_ID')
    PEA_INGRESAR = models.BooleanField(default=False, null=False, db_column='PEA_INGRESAR')
    PEA_MODIFICAR = models.BooleanField(default=False, null=False, db_column='PEA_MODIFICAR')
    PEA_ELIMINAR = models.BooleanField(default=False, null=False, db_column='PEA_ELIMINAR')
    PEA_CONSULTAR = models.BooleanField(default=False, null=False, db_column='PEA_CONSULTAR')

    class Meta:
        db_table = 'PERFIL_APLICACION'

class Aplicacion(models.Model):
    APL_ID = models.BigAutoField(primary_key=True, db_column='APL_ID')
    APL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='APL_DESCRIPCION')
    APL_VIGENTE = models.BooleanField(default=True, null=False, db_column='APL_VIGENTE')

    class Meta:
        db_table = 'APLICACION'