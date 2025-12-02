from django.db import models
from .mantenedor_model import *
from .persona_model import *
from .usuario_model import *

class Curso(models.Model):
    CUR_ID = models.BigAutoField(primary_key=True, db_column='cur_id')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usu_id')
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE, db_column='tcu_id')
    PER_ID_RESPONSABLE = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id_responsable')
    CAR_ID_RESPONSABLE = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='cargo_responsable', db_column='car_id_responsable')
    COM_ID_LUGAR = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='comuna_lugar', db_column='com_id_lugar')
    CUR_FECHA_HORA = models.DateTimeField(auto_now_add=True, db_column='cur_fecha_hora')
    CUR_FECHA_SOLICITUD = models.DateField(db_column='cur_fecha_solicitud')
    CUR_CODIGO = models.CharField(max_length=20, unique=True, db_column='cur_codigo')
    CUR_DESCRIPCION = models.CharField(max_length=255, db_column='cur_descripcion')
    CUR_OBSERVACION = models.CharField(max_length=255, blank=True, null=True, db_column='cur_observacion')
    CUR_ADMINISTRA_OPCION = [
        (1, 'Zona'),
        (2, 'Distrito'),
    ]
    CUR_ADMINISTRA = models.IntegerField(choices=CUR_ADMINISTRA_OPCION, null=False, db_column='cur_administra')
    CUR_COTA_CON_ALMUERZO = models.IntegerField(db_column='cur_cota_con_almuerzo')
    CUR_COTA_SIN_ALMUERZO = models.IntegerField(db_column='cur_cota_sin_almuerzo')
    CUR_MODALIDAD_OPTIONS = [
        (1, 'Internado'),
        (2, 'Externado'),
        (3, 'Internado/Externado'),
    ]
    CUR_MODALIDAD = models.IntegerField(choices=CUR_MODALIDAD_OPTIONS, null=False, db_column='cur_modalidad')
    CUR_TIPO_CURSO_OPTIONS = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUR_TIPO_CURSO = models.IntegerField(choices=CUR_TIPO_CURSO_OPTIONS, null=False, db_column='cur_tipo_curso')
    CUR_LUGAR = models.CharField(max_length=100, db_column='cur_lugar')
    CUR_COORD_LATITUD = models.CharField(max_length=50, null=True, db_column='cur_coord_latitud')
    CUR_COORD_LONGITUD = models.CharField(max_length=50, null=True, db_column='cur_coord_longitud')
    CUR_ESTADO_OPTIONS = [
        (0, 'Pendiente'),
        (1, 'Vigente'),
        (2, 'Anulado'),
        (3, 'Finalizado'),
    ]
    CUR_ESTADO = models.IntegerField(choices=CUR_ESTADO_OPTIONS, null=False, db_column='cur_estado')

    class Meta:
        db_table = 'curso'

class Curso_Cuota(models.Model):
    CUU_ID = models.BigAutoField(primary_key=True, db_column='cuu_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    CUU_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    CUU_TIPO = models.IntegerField(choices=CUU_TIPO_OPCION, null=False, db_column='cuu_tipo')
    CUU_FECHA = models.DateField(null=False, db_column='cuu_fecha')
    CUU_VALOR = models.DecimalField(max_digits=21,decimal_places=6, null=False, db_column='cuu_valor')

    class Meta:
        db_table = 'curso_cuota'

class Curso_Fecha(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True, db_column='cuf_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    CUF_FECHA_INICIO = models.DateField(null=False, db_column='cuf_fecha_inicio')
    CUF_FECHA_TERMINO = models.DateField(null=False, db_column='cuf_fecha_termino')
    CUF_TIPO_OPCION = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUF_TIPO = models.IntegerField(choices=CUF_TIPO_OPCION, null=False, db_column='cuf_tipo')

    class Meta:
        db_table = 'curso_fecha'

class Curso_Alimentacion(models.Model):
    CUA_ID = models.BigAutoField(primary_key=True, db_column='cua_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    ALI_ID = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, null=False, db_column='ali_id')
    CUA_FECHA = models.DateField(db_column='cua_fecha')
    CUA_TIEMPO_OPCION = [
        (1, 'Desayuno'),
        (2, 'Almuerzo'),
        (3, 'Once'),
        (4, 'Cena'),
        (5, 'Once/Cena'),
    ]
    CUA_TIEMPO = models.IntegerField(choices=CUA_TIEMPO_OPCION, null=False, db_column='cua_tiempo')
    CUA_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='cua_descripcion')
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0, null=False, db_column='cua_cantidad_adicional')
    CUA_VIGENTE = models.BooleanField(default=True, null=False, db_column='cua_vigente')

    class Meta:
        db_table = 'curso_alimentacion'

class Curso_Coordinador(models.Model):
    CUC_ID = models.BigAutoField(primary_key=True, db_column='cuc_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    CAR_ID = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='car_id')
    CUC_CARGO = models.CharField(max_length=100, null=True, db_column='cuc_cargo')

    class Meta:
        db_table = 'curso_coordinador'

class Curso_Seccion(models.Model):
    CUS_ID = models.BigAutoField(primary_key=True, db_column='cus_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    RAM_ID = models.ForeignKey(Rama, on_delete=models.PROTECT, null=True, db_column='ram_id')
    CUS_SECCION = models.IntegerField(null=False, db_column='cus_seccion')
    CUS_CANT_PARTICIPANTE = models.IntegerField(null=False, db_column='cus_cant_participante')

    class Meta:
        db_table = 'curso_seccion'

class Curso_Formador(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True, db_column='cuf_id')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    ROL_ID = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='rol_id')
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='cus_id')
    CUO_DIRECTOR = models.BooleanField(default=False, null=False, db_column='cuo_director')

    class Meta:
        db_table = 'curso_formador'
