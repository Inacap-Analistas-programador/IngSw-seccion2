from django.db import models
from .usuario_model import *
from .curso_model import *

class Archivo(models.Model):
    ARC_ID = models.BigAutoField(primary_key=True, db_column='arc_id')
    TAR_ID = models.ForeignKey('Tipo_Archivo', on_delete=models.PROTECT, null=False, db_column='tar_id')
    USU_ID_CREA = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_crea', null=False, db_column='usu_id_crea')
    USU_ID_MODIFICA = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_modifica', null=True, db_column='usu_id_modifica')
    ARC_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='arc_fecha_hora')
    ARC_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='arc_descripcion')
    ARC_RUTA = models.CharField(max_length=255, null=False, db_column='arc_ruta')
    ARC_VIGENTE = models.BooleanField(default=True, null=False, db_column='arc_vigente')

    class Meta:
        db_table = 'archivo'

class Archivo_Curso(models.Model):
    ARU_ID = models.BigAutoField(primary_key=True, db_column='aru_id')
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='arc_id')
    CUS_ID = models.ForeignKey(Curso_Seccion, on_delete=models.PROTECT, null=False, db_column='cus_id')

    class Meta:
        db_table = 'archivo_curso'

class Archivo_Persona(models.Model):
    ARP_ID = models.BigAutoField(primary_key=True, db_column='arp_id')
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='arc_id')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    CUS_ID = models.ForeignKey(Curso_Seccion, on_delete=models.CASCADE, null=True, db_column='cus_id')

    class Meta:
        db_table = 'archivo_persona'

