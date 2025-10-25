from django.db import models
from .ModuloMantenedores import *
from .ModuloUsuarios import *

class Curso(models.Model):
    CURS_ID = models.BigAutoField(primary_key=True)
    USU_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE)
    PER_ID_RESPONSABLE = models.ForeignKey(Persona, on_delete=models.CASCADE)
    CAR_ID_RESPONSABLE = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='cargo_responsable')
    COM_ID_LUGAR = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='comuna_lugar')
    CUR_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    CUR_FECHA_SOLICITUD = models.DateField()
    CUR_CODIGO = models.CharField(max_length=20, unique=True)
    CUR_DESCRIPCION = models.CharField(max_length=255)
    CUR_OBSERVACION = models.CharField(max_length=255, blank=True, null=True)
    CUR_ADMINISTRA_OPCION = [
        (2, 'Zona'),
        (2, 'Distrito'),
    ]
    CUR_ADMINISTRA = models.IntegerField(choices=CUR_ADMINISTRA_OPCION, null=False)
    CUR_COTA_CON_ALMUERZO = models.IntegerField()
    CUR_COTA_SIN_ALMUERZO = models.IntegerField()
    CUR_MODALIDAD_OPTIONS = [
        (1, 'Internado'),
        (2, 'Externado'),
        (3, 'Internado/Externado'),
    ]
    CUR_MODALIDAD = models.IntegerField(choices=CUR_MODALIDAD_OPTIONS, null=False)
    CUR_TIPO_CURSO_OPTIONS = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUR_TIPO_CURSO = models.IntegerField(choices=CUR_TIPO_CURSO_OPTIONS, null=False)
    CUR_LUGAR = models.CharField(max_length=100)
    CUR_ESTADO_OPTIONS = [
        (0, 'Pendiente'),
        (1, 'Vigente'),
        (2, 'Anulado'),
        (3, 'Finalizado'),
    ]
    CUR_ESTADO = models.IntegerField(choices=CUR_ESTADO_OPTIONS, null=False)

class Curso_Cuota(models.Model):
    CUU_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    CUU_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    CUU_TIPO = models.IntegerField(choices=CUU_TIPO_OPCION, null=False)
    CUU_FECHA = models.DateField(null=False)
    CUU_VALOR = models.DecimalField(max_digits=21,decimal_places=6, null=False)

class Curso_Fecha(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    CUF_FECHA_INICIO = models.DateField(null=False)
    CUF_FECHA_TERMINO = models.DateField(null=False)
    CUF_TIPO_OPCION = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUF_TIPO = models.IntegerField(choices=CUF_TIPO_OPCION, null=False)

class Curso_Alimentacion(models.Model):
    CUA_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    ALI_ID = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, null=False)
    CUA_FECHA = models.DateField()
    CUA_TIEMPO_OPCION = [
        (1, 'Desayuno'),
        (2, 'Almuerzo'),
        (3, 'Once'),
        (4, 'Cena'),
        (5, 'Once/Cena'),
    ]
    CUA_TIEMPO = models.IntegerField(choices=CUA_TIEMPO_OPCION, null=False)
    CUA_DESCRIPCION = models.CharField(max_length=100, null=False)
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0, null=False)
    CUA_VIGENTE = models.BooleanField(default=True, null=False)

class Curso_Coordinador(models.Model):
    CUC_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False)
    CAR_ID = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False)
    CUC_CARGO = models.CharField(max_length=100, null=True)

class Curso_Seccion(models.Model):
    CUS_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    RAM_ID = models.ForeignKey(Rama, on_delete=models.PROTECT, null=True)
    CUS_SECCION = models.IntegerField(null=False)
    CUS_CANT_PARTICIPANTE = models.IntegerField(null=False)

class Curso_Formador(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False)
    ROL_ID = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False)
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False)
    CUO_DIRECTOR = models.BooleanField(default=False, null=False)

class Tipo_Curso(models.Model):
    TCU_ID = models.BigAutoField(primary_key=True)
    TCU_DESCRIPCION = models.CharField(max_length=100, null=False)
    TCU_TIPO_OPCION = [
        (1, 'Inicial'),
        (2, 'Medio'),
        (3, 'Avanzado'),
        (4, 'Habilitación'),
        (5, 'Verificación'),
        (6, 'Institucional'),
    ]
    TCU_TIPO = models.IntegerField(choices=TCU_TIPO_OPCION, null=False)
    TCU_CANT_PARTICIPANTE = models.IntegerField(null=True)
    TCU_VIGENTE = models.BooleanField(default=True, null=False)
