from django.db import models
from .usuario_model import *
from .curso_model import *

class Archivo(models.Model):
    arc_id = models.BigAutoField(primary_key=True, db_column='arc_id')
    tar_id = models.ForeignKey('Tipo_Archivo', on_delete=models.PROTECT, null=False, db_column='tar_id')
    usu_id_crea = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_crea', null=False, db_column='usu_id_crea')
    usu_id_modifica = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='usuario_modifica', null=True, db_column='usu_id_modifica')
    arc_fecha_hora = models.DateTimeField(auto_now_add=True, null=False, db_column='arc_fecha_hora')
    arc_descripcion = models.CharField(max_length=100, null=False, db_column='arc_descripcion')
    arc_ruta = models.CharField(max_length=255, null=False, db_column='arc_ruta')
    arc_vigente = models.BooleanField(default=True, null=False, db_column='arc_vigente')

    class Meta:
        db_table = 'archivo'

class Archivo_Curso(models.Model):
    aru_id = models.BigAutoField(primary_key=True, db_column='aru_id')
    arc_id = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='arc_id')
    cus_id = models.ForeignKey(Curso_Seccion, on_delete=models.PROTECT, null=False, db_column='cus_id')

    class Meta:
        db_table = 'archivo_curso'

class Archivo_Persona(models.Model):
    arp_id = models.BigAutoField(primary_key=True, db_column='arp_id')
    arc_id = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False, db_column='arc_id')
    per_id = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    cus_id = models.ForeignKey(Curso_Seccion, on_delete=models.CASCADE, null=True, db_column='cus_id')

    class Meta:
        db_table = 'archivo_persona'
