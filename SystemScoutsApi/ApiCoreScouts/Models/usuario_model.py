from django.db import models
from .mantenedor_model import *
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(BaseUserManager):
    def create_user(self, USU_USERNAME, password=None, **extra_fields):
        if not USU_USERNAME:
            raise ValueError('El usuario debe tener un nombre de usuario (USU_USERNAME)')
        
        # Asegurar que los campos booleanos estén establecidos
        extra_fields.setdefault('USU_IS_STAFF', False)
        extra_fields.setdefault('USU_IS_SUPERUSER', False)
        extra_fields.setdefault('USU_VIGENTE', True)
        
        usuario = self.model(USU_USERNAME=USU_USERNAME, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, USU_USERNAME, password=None, **extra_fields):
        # Obtener el perfil de administrador
        from .usuario_model import Perfil
        perfil_admin, created = Perfil.objects.get_or_create(
            PEL_DESCRIPCION='Administrador', 
            defaults={'PEL_VIGENTE': True}
        )
        
        # Establecer campos requeridos para superuser
        extra_fields.setdefault('USU_IS_STAFF', True)
        extra_fields.setdefault('USU_IS_SUPERUSER', True)
        extra_fields.setdefault('USU_VIGENTE', True)
        extra_fields.setdefault('PEL_ID', perfil_admin)
        
        return self.create_user(USU_USERNAME, password, **extra_fields)

    def get_by_natural_key(self, USU_USERNAME):
        return self.get(USU_USERNAME=USU_USERNAME)

class Usuario(AbstractBaseUser, PermissionsMixin):
    USU_ID = models.BigAutoField(primary_key=True, db_column='USU_ID')
    PEL_ID = models.ForeignKey('Perfil', on_delete=models.PROTECT, null=False, db_column='PEL_ID')
    USU_USERNAME = models.CharField(max_length=100, unique=True, null=False, db_column='USU_USERNAME')
    password = models.CharField(max_length=128, null=False, db_column='USU_PASSWORD')
    
    # Campos requeridos por Django - usar nombres consistentes
    USU_IS_STAFF = models.BooleanField(default=False, db_column='USU_IS_STAFF')
    USU_IS_SUPERUSER = models.BooleanField(default=False, db_column='USU_IS_SUPERUSER')
    USU_IS_ACTIVE = models.BooleanField(default=True, db_column='USU_IS_ACTIVE')
    
    # Tus campos personalizados
    USU_RUTA_FOTO = models.CharField(max_length=255, null=True, db_column='USU_RUTA_FOTO')
    USU_VIGENTE = models.BooleanField(default=True, null=False, db_column='USU_VIGENTE')
    
    # Eliminar last_login=None ya que AbstractBaseUser lo maneja

    objects = UsuarioManager()

    USERNAME_FIELD = 'USU_USERNAME'
    REQUIRED_FIELDS = []

    # Propiedades para compatibilidad con Django
    @property
    def is_staff(self):
        return self.USU_IS_STAFF
    
    @property
    def is_superuser(self):
        return self.USU_IS_SUPERUSER
    
    @property
    def is_active(self):
        return self.USU_IS_ACTIVE and self.USU_VIGENTE

    def has_perm(self, perm, obj=None):
        return self.USU_IS_SUPERUSER

    def has_module_perms(self, app_label):
        return self.USU_IS_SUPERUSER

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_by_natural_key(self, USU_USERNAME):
        return self.__class__.objects.get(USU_USERNAME=USU_USERNAME)

    class Meta:
        db_table = 'USUARIO'

# Mantén tus otros modelos (Perfil, Perfil_Aplicacion, Aplicacion) igual
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