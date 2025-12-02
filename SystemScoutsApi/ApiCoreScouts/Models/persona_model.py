from django.db import models
from .mantenedor_model import *

class Persona(models.Model):
    PER_ID = models.BigAutoField(primary_key=True, db_column='per_id')
    ESC_ID = models.ForeignKey(Estado_Civil, on_delete=models.PROTECT, null=False, db_column='esc_id')
    COM_ID = models.ForeignKey(Comuna, on_delete=models.PROTECT, null=False, db_column='com_id')
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='usu_id')
    PER_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='per_fecha_hora')
    PER_RUN = models.CharField(max_length=9, unique=True, null=False, db_column='per_run')
    PER_DV = models.CharField(max_length=1, null=False, db_column='per_dv')
    PER_APELPTA = models.CharField(max_length=50, null=False, db_column='per_apelpta')
    PER_APELMAT = models.CharField(max_length=50, null=True, db_column='per_apelmat')
    PER_NOMBRES = models.CharField(max_length=50, null=False, db_column='per_nombres')
    PER_MAIL = models.CharField(max_length=100, null=False, db_column='per_mail')
    PER_FECHA_NAC = models.DateField(null=False, db_column='per_fecha_nac')
    PER_DIRECCION = models.CharField(max_length=255, null=False, db_column='per_direccion')
    PER_TIPO_FONO_OPTIONS = [
        (1, 'Fono Fijo'),
        (2, 'Celular'),
        (3, 'Celular/WhatsApp'),
        (4, 'WhatsApp'),
    ]
    PER_TIPO_FONO = models.IntegerField(choices=PER_TIPO_FONO_OPTIONS, null=False, db_column='per_tipo_fono')
    PER_FONO = models.CharField(max_length=15, blank=True, null=False, db_column='per_fono')
    PER_ALERGIA_ENFERMEDAD = models.CharField(max_length=255, null=True, db_column='per_alergia_enfermedad')
    PER_LIMITACION = models.CharField(max_length=255, null=True, db_column='per_limitacion')
    PER_NOM_EMERGENCIA = models.CharField(max_length=50, null=True, db_column='per_nom_emergencia')
    PER_FONO_EMERGENCIA = models.CharField(max_length=15, null=True, db_column='per_fono_emergencia')
    PER_OTROS = models.CharField(max_length=255, null=True, db_column='per_otros')
    PER_NUM_MMA = models.IntegerField(null=True, db_column='per_num_mma')
    PER_PROFESION = models.CharField(max_length=100, null=True, db_column='per_profesion')
    PER_TIEMPO_NNAJ = models.CharField(max_length=100, null=True, db_column='per_tiempo_nnaj')
    PER_TIEMPO_ADULTO = models.CharField(max_length=100, null=True, db_column='per_tiempo_adulto')
    PER_RELIGION = models.CharField(max_length=100, null=True, db_column='per_religion')
    PER_APODO = models.CharField(max_length=50, null=False, db_column='per_apodo')
    PER_FOTO = models.CharField(max_length=255, null=True, db_column='per_foto')
    PER_VIGENTE = models.BooleanField(default=True, null=False, db_column='per_vigente')

    class Meta:
        db_table = 'persona'

class Persona_Grupo(models.Model):
    PEG_ID = models.BigAutoField(primary_key=True, db_column='peg_id')
    GRU_ID = models.ForeignKey(Grupo, on_delete=models.PROTECT, null=False, db_column='gru_id')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    PEG_VIGENTE = models.BooleanField(default=True, null=False, db_column='peg_vigente')

    class Meta:
        db_table = 'persona_grupo'

class Persona_Formador(models.Model):
    PEF_ID = models.BigAutoField(primary_key=True, db_column='pef_id')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    PEF_HAB_1 = models.BooleanField(default=False, null=False, db_column='pef_hab_1')
    PEF_HAB_2 = models.BooleanField(default=False, null=False, db_column='pef_hab_2')
    PEF_VERIF = models.BooleanField(default=False, null=False, db_column='pef_verif')
    PEF_HISTORIAL = models.CharField(max_length=500, blank=True, null=True, db_column='pef_historial')

    class Meta:
        db_table = 'persona_formador'

class Persona_Individual(models.Model):
    PEI_ID = models.BigAutoField(primary_key=True, db_column='pei_id')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    CAR_ID = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='car_id')
    DIS_ID = models.ForeignKey(Distrito, on_delete=models.PROTECT, null=True, db_column='dis_id')
    ZON_ID = models.ForeignKey(Zona, on_delete=models.PROTECT, null=True, db_column='zon_id')
    PEI_VIGENTE = models.BooleanField(default=True, null=False, db_column='pei_vigente')

    class Meta:
        db_table = 'persona_individual'

class Persona_Nivel(models.Model):
    PEN_ID = models.BigAutoField(primary_key=True, db_column='pen_id')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    NIV_ID = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=False, db_column='niv_id')
    RAM_ID = models.ForeignKey(Rama, on_delete=models.PROTECT, null=False, db_column='ram_id')

    class Meta:
        db_table = 'persona_nivel'

class Persona_Curso(models.Model):
    PEC_ID = models.BigAutoField(primary_key=True, db_column='pec_id')
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='cus_id')
    ROL_ID = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='rol_id')
    ALI_ID = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, blank=True, null=True, db_column='ali_id')
    NIV_ID = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=True, db_column='niv_id')
    PEC_OBSERVACION = models.CharField(max_length=500, blank=True, null=True, db_column='pec_observacion')
    PEC_REGISTRO = models.BooleanField(default=False, null=False, db_column='pec_registro')
    PEC_ACREDITACION = models.BooleanField(default=False, null=False, db_column='pec_acreditacion')
    PEC_ENVIO_CORREO_QR = models.BooleanField(default=False, null=False, db_column='pec_envio_correo_qr')

    class Meta:
        db_table = 'persona_curso'

class Persona_Estado_Curso(models.Model):
    PEU_ID = models.BigAutoField(primary_key=True, db_column='peu_id')
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='usu_id')
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='pec_id')
    PEU_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False, db_column='peu_fecha_hora')
    PEU_ESTADO_OPTIONS = [
        (1, 'Pre Inscrito'),
        (2, 'Avisado'),
        (3, 'Lista de Espera'),
        (4, 'Inscrito'),
        (5, 'Vigente'),
        (6, 'Anulado'),
        (7, 'Sobrecupo'),
    ]
    PEU_ESTADO = models.IntegerField(choices=PEU_ESTADO_OPTIONS, null=False, db_column='peu_estado')
    PEU_VIGENTE = models.BooleanField(default=True, null=False, db_column='peu_vigente')

    class Meta:
        db_table = 'persona_estado_curso'

class Persona_Vehiculo(models.Model): 
    PEV_ID = models.BigAutoField(primary_key=True, db_column='pev_id')
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='pec_id')
    PEV_MARCA = models.CharField(max_length=50, null=False, db_column='pev_marca')
    PEV_MODELO = models.CharField(max_length=50, null=False, db_column='pev_modelo')
    PEV_PATENTE = models.CharField(max_length=10, null=False, db_column='pev_patente')

    class Meta:
        db_table = 'persona_vehiculo'