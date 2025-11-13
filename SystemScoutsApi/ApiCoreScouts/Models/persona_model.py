from django.db import models
from .mantenedor_model import *

class Persona(models.Model):
    PER_ID = models.BigAutoField(primary_key=True, db_column='PER_ID')
    ESC_ID = models.ForeignKey(Estado_Civil, on_delete=models.PROTECT, null=False, db_column='ESC_ID')
    COM_ID = models.ForeignKey(Comuna, on_delete=models.PROTECT, null=False, db_column='COM_ID')
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='USU_ID')
    PER_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='PER_FECHA_HORA')
    PER_RUN = models.CharField(max_length=9, unique=True, null=False, db_column='PER_RUN')
    PER_DV = models.CharField(max_length=1, null=False, db_column='PER_DV')
    PER_APELPTA = models.CharField(max_length=50, null=False, db_column='PER_APELPTA')
    PER_APELMAT = models.CharField(max_length=50, null=True, db_column='PER_APELMAT')
    PER_NOMBRES = models.CharField(max_length=50, null=False, db_column='PER_NOMBRES')
    PER_MAIL = models.CharField(max_length=100, null=False, db_column='PER_MAIL')
    PER_FECHA_NAC = models.DateField(null=False, db_column='PER_FECHA_NAC')
    PER_DIRECCION = models.CharField(max_length=255, null=False, db_column='PER_DIRECCION')
    PER_TIPO_FONO_OPTIONS = [
        (1, 'Fono Fijo'),
        (2, 'Celular'),
        (3, 'Celular/WhatsApp'),
        (4, 'WhatsApp'),
    ]
    PER_TIPO_FONO = models.IntegerField(choices=PER_TIPO_FONO_OPTIONS, null=False, db_column='PER_TIPO_FONO')
    PER_FONO = models.CharField(max_length=15, blank=True, null=False, db_column='PER_FONO')
    PER_ALERGIA_ENFERMEDAD = models.CharField(max_length=255, null=True, db_column='PER_ALERGIA_ENFERMEDAD')
    PER_LIMITACION = models.CharField(max_length=255, null=True, db_column='PER_LIMITACION')
    PER_NOM_EMERGENCIA = models.CharField(max_length=50, null=True, db_column='PER_NOM_EMERGENCIA')
    PER_FONO_EMERGENCIA = models.CharField(max_length=15, null=True, db_column='PER_FONO_EMERGENCIA')
    PER_OTROS = models.CharField(max_length=255, null=True, db_column='PER_OTROS')
    PER_NUM_MMA = models.IntegerField(null=True, db_column='PER_NUM_MMA')
    PER_PROFESION = models.CharField(max_length=100, null=True, db_column='PER_PROFESION')
    PER_TIEMPO_NNAJ = models.CharField(max_length=100, null=True, db_column='PER_TIEMPO_NNAJ')
    PER_TIEMPO_ADULTO = models.CharField(max_length=100, null=True, db_column='PER_TIEMPO_ADULTO')
    PER_RELIGION = models.CharField(max_length=100, null=True, db_column='PER_RELIGION')
    PER_APODO = models.CharField(max_length=50, null=False, db_column='PER_APODO')
    PER_FOTO = models.CharField(max_length=255, null=True, db_column='PER_FOTO')
    PER_VIGENTE = models.BooleanField(default=True, null=False, db_column='PER_VIGENTE')

    class Meta:
        db_table = 'PERSONA'

class Persona_Grupo(models.Model):
    PEG_ID = models.BigAutoField(primary_key=True, db_column='PEG_ID')
    GRU_ID = models.ForeignKey(Grupo, on_delete=models.PROTECT, null=False, db_column='GRU_ID')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='PER_ID')
    PEG_VIGENTE = models.BooleanField(default=True, null=False, db_column='PEG_VIGENTE')

    class Meta:
        db_table = 'PERSONA_GRUPO'

class Persona_Formador(models.Model):
    PEF_ID = models.BigAutoField(primary_key=True, db_column='PEF_ID')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='PER_ID')
    PEF_HAB_1 = models.BooleanField(default=False, null=False, db_column='PEF_HAB_1')
    PEF_HAB_2 = models.BooleanField(default=False, null=False, db_column='PEF_HAB_2')
    PEF_VERIF = models.BooleanField(default=False, null=False, db_column='PEF_VERIF')
    PEF_HISTORIAL = models.CharField(max_length=500, blank=True, null=True, db_column='PEF_HISTORIAL')

    class Meta:
        db_table = 'PERSONA_FORMADOR'

class Persona_Individual(models.Model):
    PEI_ID = models.BigAutoField(primary_key=True, db_column='PEI_ID')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CAR_ID = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='CAR_ID')
    DIS_ID = models.ForeignKey(Distrito, on_delete=models.PROTECT, null=True, db_column='DIS_ID')
    ZON_ID = models.ForeignKey(Zona, on_delete=models.PROTECT, null=True, db_column='ZON_ID')
    PEI_VIGENTE = models.BooleanField(default=True, null=False, db_column='PEI_VIGENTE')

    class Meta:
        db_table = 'PERSONA_INDIVIDUAL'

class Persona_Nivel(models.Model):
    PEN_ID = models.BigAutoField(primary_key=True, db_column='PEN_ID')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='PER_ID')
    NIV_ID = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=False, db_column='NIV_ID')
    RAM_ID = models.ForeignKey(Rama, on_delete=models.PROTECT, null=False, db_column='RAM_ID')

    class Meta:
        db_table = 'PERSONA_NIVEL'

class Persona_Curso(models.Model):
    PEC_ID = models.BigAutoField(primary_key=True, db_column='PEC_ID')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='CUS_ID')
    ROL_ID = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='ROL_ID')
    ALI_ID = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, blank=True, null=True, db_column='ALI_ID')
    NIV_ID = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=True, db_column='NIV_ID')
    PEC_OBSERVACION = models.CharField(max_length=500, blank=True, null=True, db_column='PEC_OBSERVACION')
    PEC_REGISTRO = models.BooleanField(default=False, null=False, db_column='PEC_REGISTRO')
    PEC_ACREDITACION = models.BooleanField(default=False, null=False, db_column='PEC_ACREDITACION')
    PEC_ENVIO_CORREO_QR = models.BooleanField(default=False, null=False, db_column='PEC_ENVIO_CORREO_QR')

    class Meta:
        db_table = 'PERSONA_CURSO'

class Persona_Estado_Curso(models.Model):
    PEU_ID = models.BigAutoField(primary_key=True, db_column='PEU_ID')
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='USU_ID')
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='PEC_ID')
    PEU_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='PEU_FECHA_HORA')
    PEU_ESTADO_OPTIONS = [
        (1, 'Pre Inscrito'),
        (2, 'Avisado'),
        (3, 'Lista de Espera'),
        (4, 'Inscrito'),
        (5, 'Vigente'),
        (6, 'Anulado'),
        (7, 'Sobrecupo'),
    ]
    PEU_ESTADO = models.IntegerField(choices=PEU_ESTADO_OPTIONS, null=False, db_column='PEU_ESTADO')
    PEU_VIGENTE = models.BooleanField(default=True, null=False, db_column='PEU_VIGENTE')

    class Meta:
        db_table = 'PERSONA_ESTADO_CURSO'

class Persona_Vehiculo(models.Model): 
    PEV_ID = models.BigAutoField(primary_key=True, db_column='PEV_ID')
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='PEC_ID')
    PEV_MARCA = models.CharField(max_length=50, null=False, db_column='PEV_MARCA')
    PEV_MODELO = models.CharField(max_length=50, null=False, db_column='PEV_MODELO')
    PEV_PATENTE = models.CharField(max_length=10, null=False, db_column='PEV_PATENTE')

    class Meta:
        db_table = 'PERSONA_VEHICULO'