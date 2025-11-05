from django.db import models
from .ModuloMantenedores import *
from .ModuloPersonas import *
from .ModuloUsuarios import *

class Curso(models.Model):
    CUR_ID = models.BigAutoField(primary_key=True, db_column='CUR_ID')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='USU_ID')
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE, db_column='TCU_ID')
    PER_ID_RESPONSABLE = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='PER_ID_RESPONSABLE')
    CAR_ID_RESPONSABLE = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='cargo_responsable', db_column='CAR_ID_RESPONSABLE')
    COM_ID_LUGAR = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='comuna_lugar', db_column='COM_ID_LUGAR')
    CUR_FECHA_HORA = models.DateTimeField(auto_now_add=True, db_column='CUR_FECHA_HORA')
    CUR_FECHA_SOLICITUD = models.DateField(db_column='CUR_FECHA_SOLICITUD')
    CUR_CODIGO = models.CharField(max_length=20, unique=True, db_column='CUR_CODIGO')
    CUR_DESCRIPCION = models.CharField(max_length=255, db_column='CUR_DESCRIPCION')
    CUR_OBSERVACION = models.CharField(max_length=255, blank=True, null=True, db_column='CUR_OBSERVACION')
    CUR_ADMINISTRA_OPCION = [
        (1, 'Zona'),
        (2, 'Distrito'),
    ]
    CUR_ADMINISTRA = models.IntegerField(choices=CUR_ADMINISTRA_OPCION, null=False, db_column='CUR_ADMINISTRA')
    CUR_COTA_CON_ALMUERZO = models.IntegerField(db_column='CUR_COTA_CON_ALMUERZO')
    CUR_COTA_SIN_ALMUERZO = models.IntegerField(db_column='CUR_COTA_SIN_ALMUERZO')
    CUR_MODALIDAD_OPTIONS = [
        (1, 'Internado'),
        (2, 'Externado'),
        (3, 'Internado/Externado'),
    ]
    CUR_MODALIDAD = models.IntegerField(choices=CUR_MODALIDAD_OPTIONS, null=False, db_column='CUR_MODALIDAD')
    CUR_TIPO_CURSO_OPTIONS = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUR_TIPO_CURSO = models.IntegerField(choices=CUR_TIPO_CURSO_OPTIONS, null=False, db_column='CUR_TIPO_CURSO')
    CUR_LUGAR = models.CharField(max_length=100, db_column='CUR_LUGAR')
    CUR_COORD_LATITUD = models.CharField(max_length=50, null=True, db_column='CUR_COORD_LATITUD')
    CUR_COORD_LONGITUD = models.CharField(max_length=50, null=True, db_column='CUR_COORD_LONGITUD')
    CUR_ESTADO_OPTIONS = [
        (0, 'Pendiente'),
        (1, 'Vigente'),
        (2, 'Anulado'),
        (3, 'Finalizado'),
    ]
    CUR_ESTADO = models.IntegerField(choices=CUR_ESTADO_OPTIONS, null=False, db_column='CUR_ESTADO')

    class Meta:
        db_table = 'CURSO'

class Curso_Cuota(models.Model):
    CUU_ID = models.BigAutoField(primary_key=True, db_column='CUU_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    CUU_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    CUU_TIPO = models.IntegerField(choices=CUU_TIPO_OPCION, null=False, db_column='CUU_TIPO')
    CUU_FECHA = models.DateField(null=False, db_column='CUU_FECHA')
    CUU_VALOR = models.DecimalField(max_digits=21,decimal_places=6, null=False, db_column='CUU_VALOR')

    class Meta:
        db_table = 'CURSO_CUOTA'

class Curso_Fecha(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True, db_column='CUF_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    CUF_FECHA_INICIO = models.DateField(null=False, db_column='CUF_FECHA_INICIO')
    CUF_FECHA_TERMINO = models.DateField(null=False, db_column='CUF_FECHA_TERMINO')
    CUF_TIPO_OPCION = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUF_TIPO = models.IntegerField(choices=CUF_TIPO_OPCION, null=False, db_column='CUF_TIPO')

    class Meta:
        db_table = 'CURSO_FECHA'

class Curso_Alimentacion(models.Model):
    CUA_ID = models.BigAutoField(primary_key=True, db_column='CUA_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    ALI_ID = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, null=False, db_column='ALI_ID')
    CUA_FECHA = models.DateField(db_column='CUA_FECHA')
    CUA_TIEMPO_OPCION = [
        (1, 'Desayuno'),
        (2, 'Almuerzo'),
        (3, 'Once'),
        (4, 'Cena'),
        (5, 'Once/Cena'),
    ]
    CUA_TIEMPO = models.IntegerField(choices=CUA_TIEMPO_OPCION, null=False, db_column='CUA_TIEMPO')
    CUA_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='CUA_DESCRIPCION')
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0, null=False, db_column='CUA_CANTIDAD_ADICIONAL')
    CUA_VIGENTE = models.BooleanField(default=True, null=False, db_column='CUA_VIGENTE')

    class Meta:
        db_table = 'CURSO_ALIMENTACION'

class Curso_Coordinador(models.Model):
    CUC_ID = models.BigAutoField(primary_key=True, db_column='CUC_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CAR_ID = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='CAR_ID')
    CUC_CARGO = models.CharField(max_length=100, null=True, db_column='CUC_CARGO')

    class Meta:
        db_table = 'CURSO_COORDINADOR'

class Curso_Seccion(models.Model):
    CUS_ID = models.BigAutoField(primary_key=True, db_column='CUS_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    RAM_ID = models.ForeignKey(Rama, on_delete=models.PROTECT, null=True, db_column='RAM_ID')
    CUS_SECCION = models.IntegerField(null=False, db_column='CUS_SECCION')
    CUS_CANT_PARTICIPANTE = models.IntegerField(null=False, db_column='CUS_CANT_PARTICIPANTE')

    class Meta:
        db_table = 'CURSO_SECCION'

class Curso_Formador(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True, db_column='CUF_ID')
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='PER_ID')
    ROL_ID = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='ROL_ID')
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='CUS_ID')
    CUO_DIRECTOR = models.BooleanField(default=False, null=False, db_column='CUO_DIRECTOR')

    class Meta:
        db_table = 'CURSO_FORMADOR'
