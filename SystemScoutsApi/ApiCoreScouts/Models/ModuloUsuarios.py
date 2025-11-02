from django.db import models
from .ModuloMantenedores import *
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(USU_USERNAME=username)

class Usuario(models.Model):
    USU_ID = models.BigAutoField(primary_key=True, db_column='USU_ID')
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False, db_column='PEL_ID')
    USU_USERNAME = models.CharField(max_length=100, unique=True, null=False, db_column='USU_USERNAME')
    USU_PASSWORD = models.CharField(max_length=128, null=False, db_column='USU_PASSWORD')
    USU_RUTA_FOTO = models.CharField(max_length=255, null=False, db_column='USU_RUTA_FOTO')
    USU_VIGENTE = models.BooleanField(default=True, null=False, db_column='USU_VIGENTE')

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