from django.db import models
from .mantenedor_model import *
from .persona_model import *
from .usuario_model import *

class Curso(models.Model):
    cur_id = models.BigAutoField(primary_key=True, db_column='cur_id')
    usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usu_id')
    tcu_id = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE, db_column='tcu_id')
    per_id_responsable = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id_responsable')
    car_id_responsable = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='cargo_responsable', db_column='car_id_responsable')
    com_id_lugar = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='comuna_lugar', db_column='com_id_lugar')
    cur_fecha_hora = models.DateTimeField(auto_now_add=True, db_column='cur_fecha_hora')
    cur_fecha_solicitud = models.DateField(db_column='cur_fecha_solicitud')
    cur_codigo = models.CharField(max_length=20, unique=True, db_column='cur_codigo')
    cur_descripcion = models.CharField(max_length=255, db_column='cur_descripcion')
    cur_observacion = models.CharField(max_length=255, blank=True, null=True, db_column='cur_observacion')
    cur_administra_opcion = [
        (1, 'Zona'),
        (2, 'Distrito'),
    ]
    cur_administra = models.IntegerField(choices=cur_administra_opcion, null=False, db_column='cur_administra')
    cur_cota_con_almuerzo = models.IntegerField(db_column='cur_cota_con_almuerzo')
    cur_cota_sin_almuerzo = models.IntegerField(db_column='cur_cota_sin_almuerzo')
    cur_modalidad_options = [
        (1, 'Internado'),
        (2, 'Externado'),
        (3, 'Internado/Externado'),
    ]
    cur_modalidad = models.IntegerField(choices=cur_modalidad_options, null=False, db_column='cur_modalidad')
    cur_tipo_curso_options = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    cur_tipo_curso = models.IntegerField(choices=cur_tipo_curso_options, null=False, db_column='cur_tipo_curso')
    cur_lugar = models.CharField(max_length=100, db_column='cur_lugar')
    cur_coord_latitud = models.CharField(max_length=50, null=True, db_column='cur_coord_latitud')
    cur_coord_longitud = models.CharField(max_length=50, null=True, db_column='cur_coord_longitud')
    cur_estado_options = [
        (0, 'Pendiente'),
        (1, 'Vigente'),
        (2, 'Anulado'),
        (3, 'Finalizado'),
    ]
    cur_estado = models.IntegerField(choices=cur_estado_options, null=False, db_column='cur_estado')

    class Meta:
        db_table = 'curso'

class Curso_Cuota(models.Model):
    cuu_id = models.BigAutoField(primary_key=True, db_column='cuu_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    cuu_tipo_opcion = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    cuu_tipo = models.IntegerField(choices=cuu_tipo_opcion, null=False, db_column='cuu_tipo')
    cuu_fecha = models.DateField(null=False, db_column='cuu_fecha')
    cuu_valor = models.DecimalField(max_digits=21,decimal_places=6, null=False, db_column='cuu_valor')

    class Meta:
        db_table = 'curso_cuota'

class Curso_Fecha(models.Model):
    cuf_id = models.BigAutoField(primary_key=True, db_column='cuf_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    cuf_fecha_inicio = models.DateField(null=False, db_column='cuf_fecha_inicio')
    cuf_fecha_termino = models.DateField(null=False, db_column='cuf_fecha_termino')
    cuf_tipo_opcion = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    cuf_tipo = models.IntegerField(choices=cuf_tipo_opcion, null=False, db_column='cuf_tipo')

    class Meta:
        db_table = 'curso_fecha'

class Curso_Alimentacion(models.Model):
    cua_id = models.BigAutoField(primary_key=True, db_column='cua_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    ali_id = models.ForeignKey(Alimentacion, on_delete=models.PROTECT, null=False, db_column='ali_id')
    cua_fecha = models.DateField(db_column='cua_fecha')
    cua_tiempo_opcion = [
        (1, 'Desayuno'),
        (2, 'Almuerzo'),
        (3, 'Once'),
        (4, 'Cena'),
        (5, 'Once/Cena'),
    ]
    cua_tiempo = models.IntegerField(choices=cua_tiempo_opcion, null=False, db_column='cua_tiempo')
    cua_descripcion = models.CharField(max_length=100, null=False, db_column='cua_descripcion')
    cua_cantidad_adicional = models.IntegerField(default=0, null=False, db_column='cua_cantidad_adicional')
    cua_vigente = models.BooleanField(default=True, null=False, db_column='cua_vigente')

    class Meta:
        db_table = 'curso_alimentacion'

class Curso_Coordinador(models.Model):
    cuc_id = models.BigAutoField(primary_key=True, db_column='cuc_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    per_id = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    car_id = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=False, db_column='car_id')
    cuc_cargo = models.CharField(max_length=100, null=True, db_column='cuc_cargo')

    class Meta:
        db_table = 'curso_coordinador'

class Curso_Seccion(models.Model):
    cus_id = models.BigAutoField(primary_key=True, db_column='cus_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    ram_id = models.ForeignKey(Rama, on_delete=models.PROTECT, null=True, db_column='ram_id')
    cus_seccion = models.IntegerField(null=False, db_column='cus_seccion')
    cus_cant_participante = models.IntegerField(null=False, db_column='cus_cant_participante')

    class Meta:
        db_table = 'curso_seccion'

class Curso_Formador(models.Model):
    cuf_id = models.BigAutoField(primary_key=True, db_column='cuf_id')
    cur_id = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False, db_column='cur_id')
    per_id = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    rol_id = models.ForeignKey(Rol, on_delete=models.PROTECT, null=False, db_column='rol_id')
    cus_id = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False, db_column='cus_id')
    cuo_director = models.BooleanField(default=False, null=False, db_column='cuo_director')

    class Meta:
        db_table = 'curso_formador'
