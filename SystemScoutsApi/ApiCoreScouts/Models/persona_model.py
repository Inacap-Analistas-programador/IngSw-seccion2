from django.db import models
from .mantenedor_model import *

class Persona(models.Model):
    per_id = models.BigAutoField(primary_key=True, db_column='per_id')
    esc_id = models.ForeignKey(Estado_Civil, on_delete=models.PROTECT, null=False, db_column='esc_id')
    com_id = models.ForeignKey(Comuna, on_delete=models.PROTECT, null=False, db_column='com_id')
    usu_id = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='usu_id')
    per_fecha_hora = models.DateTimeField(auto_now_add=True, null=False, db_column='per_fecha_hora')
    per_run = models.CharField(max_length=9, unique=True, null=False, db_column='per_run')
    per_dv = models.CharField(max_length=1, null=False, db_column='per_dv')
    per_apelpta = models.CharField(max_length=50, null=False, db_column='per_apelpat')
    per_apelmat = models.CharField(max_length=50, null=True, db_column='per_apelmat')
    per_nombres = models.CharField(max_length=50, null=False, db_column='per_nombres')
    per_mail = models.CharField(max_length=100, null=False, db_column='per_email')
    per_fecha_nac = models.DateTimeField(null=False, db_column='per_fecha_nac')
    per_direccion = models.CharField(max_length=255, null=False, db_column='per_direccion')
    per_tipo_fono_options = [
        (1, 'Fono Fijo'),
        (2, 'Celular'),
        (3, 'Celular/WhatsApp'),
        (4, 'WhatsApp'),
    ]
    per_tipo_fono = models.IntegerField(choices=per_tipo_fono_options, null=False, db_column='per_tipo_fono')
    per_fono = models.CharField(max_length=15, blank=True, null=False, db_column='per_fono')
    per_alergia_enfermedad = models.CharField(max_length=255, null=True, db_column='per_alergia_enfermedad')
    per_limitacion = models.CharField(max_length=255, null=True, db_column='per_limitacion')
    per_nom_emergencia = models.CharField(max_length=50, null=True, db_column='per_nom_emergencia')
    per_fono_emergencia = models.CharField(max_length=15, null=True, db_column='per_fono_emergencia')
    per_otros = models.CharField(max_length=255, null=True, db_column='per_otros')
    per_num_mma = models.IntegerField(null=True, db_column='per_num_mmaa')
    per_profesion = models.CharField(max_length=100, null=True, db_column='per_profesion')
    per_tiempo_nnaj = models.CharField(max_length=100, null=True, db_column='per_tiempo_nnaj')
    per_tiempo_adulto = models.CharField(max_length=100, null=True, db_column='per_tiempo_adulto')
    per_religion = models.CharField(max_length=100, null=True, db_column='per_religion')
    per_apodo = models.CharField(max_length=50, null=False, db_column='per_apodo')
    per_foto = models.CharField(max_length=255, null=True, db_column='per_foto')
    per_vigente = models.BooleanField(default=True, null=False, db_column='per_vigente')

    class Meta:
        db_table = 'persona'

class Persona_Grupo(models.Model):
    peg_id = models.BigAutoField(primary_key=True, db_column='peg_id')
    gru_id = models.ForeignKey(Grupo, on_delete=models.PROTECT, null=False, db_column='gru_id')
    per_id = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    peg_vigente = models.BooleanField(default=True, null=False, db_column='peg_vigente')

    class Meta:
        db_table = 'persona_grupo'

class Persona_Formador(models.Model):
    pef_id = models.BigAutoField(primary_key=True, db_column='pef_id')
    per_id = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    pef_hab_1 = models.BooleanField(default=False, null=False, db_column='pef_hab_1')
    pef_hab_2 = models.BooleanField(default=False, null=False, db_column='pef_hab_2')
    pef_verif = models.BooleanField(default=False, null=False, db_column='pef_verif')
    pef_historial = models.CharField(max_length=500, blank=True, null=True, db_column='pef_historial')

    class Meta:
        db_table = 'persona_formador'

class Persona_Individual(models.Model):
    pei_id = models.BigAutoField(primary_key=True, db_column='pei_id')
    per_id = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    car_id = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='car_id')
    dis_id = models.ForeignKey(Distrito, on_delete=models.PROTECT, null=True, db_column='dis_id')
    zon_id = models.ForeignKey(Zona, on_delete=models.PROTECT, null=True, db_column='zon_id')
    pei_vigente = models.BooleanField(default=True, null=False, db_column='pei_vigente')

    class Meta:
        db_table = 'persona_individual'

class Persona_Nivel(models.Model):
    pen_id = models.BigAutoField(primary_key=True, db_column='pen_id')
    per_id = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    niv_id = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=False, db_column='niv_id')
    ram_id = models.ForeignKey(Rama, on_delete=models.PROTECT, null=False, db_column='ram_id')

    class Meta:
        db_table = 'persona_nivel'

class Persona_Curso(models.Model):
    pec_id = models.BigAutoField(primary_key=True, db_column='pec_id')
    per_id = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False, db_column='per_id')
    cus_id = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='cus_id')
    rol_id = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='rol_id')
    ali_id = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, blank=True, null=True, db_column='ali_id')
    niv_id = models.ForeignKey(Nivel, on_delete=models.PROTECT, null=True, db_column='niv_id')
    pec_observacion = models.CharField(max_length=500, blank=True, null=True, db_column='pec_observacion')
    pec_registro = models.BooleanField(default=False, null=False, db_column='pec_registro')
    pec_acreditacion = models.BooleanField(default=False, null=False, db_column='pec_acreditado')
    pec_envio_correo_qr = models.BooleanField(default=False, null=False, db_column='pec_envio_correo_qr')

    class Meta:
        db_table = 'persona_curso'

class Persona_Estado_Curso(models.Model):
    peu_id = models.BigAutoField(primary_key=True, db_column='peu_id')
    usu_id = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False, db_column='usu_id')
    pec_id = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='pec_id')
    peu_fecha_hora = models.DateTimeField(auto_now_add=True, null=False, db_column='peu_fecha_hora')
    peu_estado_options = [
        (1, 'Pre Inscrito'),
        (2, 'Avisado'),
        (3, 'Lista de Espera'),
        (4, 'Inscrito'),
        (5, 'Vigente'),
        (6, 'Anulado'),
        (7, 'Sobrecupo'),
    ]
    peu_estado = models.IntegerField(choices=peu_estado_options, null=False, db_column='peu_estado')
    peu_vigente = models.BooleanField(default=True, null=False, db_column='peu_vigente')

    class Meta:
        db_table = 'persona_estado_curso'

class Persona_Vehiculo(models.Model): 
    pev_id = models.BigAutoField(primary_key=True, db_column='pev_id')
    pec_id = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False, db_column='pec_id')
    pev_marca = models.CharField(max_length=50, null=False, db_column='pev_marca')
    pev_modelo = models.CharField(max_length=50, null=False, db_column='pev_modelo')
    pev_patente = models.CharField(max_length=10, null=False, db_column='pev_patente')

    class Meta:
        db_table = 'persona_vehiculo'