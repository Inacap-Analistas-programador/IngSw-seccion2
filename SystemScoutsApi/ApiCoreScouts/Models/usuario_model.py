from django.db import models
from .mantenedor_model import *
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(BaseUserManager):
    def create_user(self, usu_username, password=None, **extra_fields):
        if not usu_username:
            raise ValueError('El usuario debe tener un nombre de usuario (usu_username)')
        usuario = self.model(usu_username=usu_username, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usu_username, password=None, **extra_fields):
        from .usuario_model import Perfil  

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('usu_vigente', True)

        if 'pel_id' not in extra_fields or extra_fields['pel_id'] is None:
            perfil_admin, _ = Perfil.objects.get_or_create(PEL_DESCRIPCION='Administrador', defaults={'pel_vigente': True})
            extra_fields['pel_id'] = perfil_admin

        return self.create_user(usu_username, password, **extra_fields)

    def get_by_natural_key(self, usu_username):
        return self.get(usu_username=usu_username)

class Usuario(AbstractBaseUser, PermissionsMixin):
    usu_id = models.BigAutoField(primary_key=True, db_column='usu_id')
    pel_id = models.ForeignKey('Perfil', on_delete=models.PROTECT, null=False, db_column='pel_id')
    usu_username = models.CharField(max_length=100, unique=True, null=False, db_column='usu_username')
    password = models.CharField(max_length=128, null=False, db_column='usu_password')
    last_login = None
    usu_ruta_foto = models.CharField(max_length=255, null=True, db_column='usu_ruta_foto')
    usu_vigente = models.BooleanField(default=True, null=False, db_column='usu_vigente')
    is_staff = models.BooleanField(default=False, db_column='usu_is_staff')
    is_superuser = models.BooleanField(default=False, db_column='usu_is_superuser')

    objects = UsuarioManager()

    USERNAME_FIELD = 'usu_username'
    REQUIRED_FIELDS = []

    @property
    def is_active(self):
        return self.usu_vigente

    @property
    def id(self):
        return self.usu_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = 'usuario'

class Perfil(models.Model):
    PEL_ID = models.BigAutoField(primary_key=True, db_column='pel_id')
    PEL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='pel_descripcion')
    PEL_VIGENTE = models.BooleanField(default=True, null=False, db_column='pel_vigente')

    class Meta:
        db_table = 'perfil'

class Perfil_Aplicacion(models.Model):
    PEA_ID = models.BigAutoField(primary_key=True, db_column='pea_id')
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False, db_column='pel_id')
    APL_ID = models.ForeignKey('Aplicacion',on_delete=models.PROTECT, null=False, db_column='apl_id')
    PEA_INGRESAR = models.BooleanField(default=False, null=False, db_column='pea_ingresar')
    PEA_MODIFICAR = models.BooleanField(default=False, null=False, db_column='pea_modificar')
    PEA_ELIMINAR = models.BooleanField(default=False, null=False, db_column='pea_eliminar')
    PEA_CONSULTAR = models.BooleanField(default=False, null=False, db_column='pea_consultar')

    class Meta:
        db_table = 'perfil_aplicacion'

class Aplicacion(models.Model):
    APL_ID = models.BigAutoField(primary_key=True, db_column='apl_id')
    APL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='apl_descripcion')
    APL_VIGENTE = models.BooleanField(default=True, null=False, db_column='apl_vigente')

    class Meta:
        db_table = 'aplicacion'