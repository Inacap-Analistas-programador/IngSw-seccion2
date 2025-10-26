from django.db import models
from .ModuloUsuarios import *
from .ModuloCursos import *

class Archivo(models.Model):
    ARC_ID = models.BigAutoField(primary_key=True,db_column='ARC_ID')
    TAR_ID = models.ForeignKey('Tipo_Archivo', on_delete=models.PROTECT, null=False, db_column='TAR_ID')
    USU_ID_CREA = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_crea', null=False, db_column='USU_ID_CREA')
    USU_ID_MODIFICA = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_modifica', null=True, db_column='USU_ID_MODIFICA')
    ARC_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='ARC_FECHA_HORA')
    ARC_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='ARC_DESCRIPCION')
    ARC_RUTA = models.CharField(max_length=255, null=False, db_column='ARC_RUTA')
    ARC_VIGENTE = models.BooleanField(default=True, null=False, db_column='ARC_VIGENTE')

    class Meta:
        db_table = 'ARCHIVO'

class Archivo_Curso(models.Model):
    ARU_ID = models.BigAutoField(primary_key=True, db_column='ARU_ID')
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='ARC_ID')
    CUS_ID = models.ForeignKey(Curso_Seccion, on_delete=models.PROTECT, null=False, db_column='CUS_ID')

    class Meta:
        db_table = 'ARCHIVO_CURSO'

class Archivo_Persona(models.Model):
    ARP_ID = models.BigAutoField(primary_key=True, db_column='ARP_ID')
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='ARC_ID')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CUS_ID = models.ForeignKey(Curso_Seccion, on_delete=models.CASCADE, null=True, db_column='CUS_ID')

    class Meta:
        db_table = 'ARCHIVO_PERSONA'

