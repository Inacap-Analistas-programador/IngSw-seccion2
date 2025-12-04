from django.db import models

class Rol(models.Model):
    rol_id = models.BigAutoField(primary_key=True, db_column='rol_id')
    rol_descripcion = models.CharField(max_length=50, null=False, db_column='rol_descripcion')
    rol_tipo_options = [
        (1, 'Participante'),
        (2, 'Formadores'),
        (3, 'Apoyo Formadores'),
        (4, 'Organización'),
        (5, 'Servicio'),
        (6, 'Salud'),
    ]
    rol_tipo = models.IntegerField(choices=rol_tipo_options, null=False, db_column='rol_tipo')
    rol_vigente = models.BooleanField(default=True, null=False, db_column='rol_vigente')

    class Meta:
        db_table = 'rol'

class Cargo(models.Model):
    car_id = models.BigAutoField(primary_key=True, db_column='car_id')
    car_descripcion = models.CharField(max_length=100, null=False, db_column='car_descripcion')
    car_vigente = models.BooleanField(default=True, null=False, db_column='car_vigente')

    class Meta:
        db_table = 'cargo'

class Rama(models.Model):
    ram_id = models.BigAutoField(primary_key=True, db_column='ram_id')
    ram_descripcion = models.CharField(max_length=50, null=False, db_column='ram_descripcion')
    ram_vigente = models.BooleanField(default=True, null=False, db_column='ram_vigente')

    class Meta:
        db_table = 'rama'

class Estado_Civil(models.Model):
    esc_id = models.BigAutoField(primary_key=True, db_column='esc_id')
    esc_descripcion = models.CharField(max_length=50, null=False, db_column='esc_descripcion')
    esc_vigente = models.BooleanField(default=True, null=False, db_column='esc_vigente')

    class Meta:
        db_table = 'estado_civil'

class Nivel(models.Model):
    niv_id = models.BigAutoField(primary_key=True, db_column='niv_id')
    niv_descripcion = models.CharField(max_length=50, null=False, db_column='niv_descripcion')
    niv_orden = models.IntegerField(null=False, db_column='niv_orden')
    niv_vigente = models.BooleanField(default=True, null=False, db_column='niv_vigente')

    class Meta:
        db_table = 'nivel'

class Zona(models.Model):
    zon_id = models.BigAutoField(primary_key=True, db_column='zon_id')
    zon_descripcion = models.CharField(max_length=100, null=False, db_column='zon_descripcion')
    zon_unilateral = models.BooleanField(default=False, null=False, db_column='zon_unilateral')
    zon_vigente = models.BooleanField(default=True, null=False, db_column='zon_vigente')

    class Meta:
        db_table = 'zona'

class Distrito(models.Model):
    dis_id = models.BigAutoField(primary_key=True, db_column='dis_id')
    zon_id = models.ForeignKey('Zona', on_delete=models.PROTECT, null=False, db_column='zon_id')
    dis_descripcion = models.CharField(max_length=100, null=False, db_column='dis_descripcion')
    dis_vigente = models.BooleanField(default=True, null=False, db_column='dis_vigente')

    class Meta:
        db_table = 'distrito'

class Grupo(models.Model):
    gru_id = models.BigAutoField(primary_key=True, db_column='gru_id')
    dis_id = models.ForeignKey('Distrito', on_delete=models.PROTECT, null=False, db_column='dis_id')
    gru_descripcion = models.CharField(max_length=100, null=False, db_column='gru_descripcion')
    gru_vigente = models.BooleanField(default=True, null=False, db_column='gru_vigente')

    class Meta:
        db_table = 'grupo'

class Region(models.Model):
    reg_id = models.BigAutoField(primary_key=True, db_column='reg_id')
    reg_descripcion = models.CharField(max_length=100, null=False, db_column='reg_descripcion')
    reg_vigente = models.BooleanField(default=True, null=False, db_column='reg_vigente')

    class Meta:
        db_table = 'region'

class Provincia(models.Model):
    pro_id = models.BigAutoField(primary_key=True, db_column='pro_id')
    reg_id = models.ForeignKey('Region',on_delete=models.PROTECT, null=False, db_column='reg_id')
    pro_descripcion = models.CharField(max_length=100, null=False, db_column='pro_descripcion')
    pro_vigente = models.BooleanField(default=True, null=False, db_column='pro_vigente')

    class Meta:
        db_table = 'provincia'

class Comuna(models.Model):
    com_id = models.BigAutoField(primary_key=True, db_column='com_id')
    pro_id = models.ForeignKey('Provincia',on_delete=models.PROTECT, null=False, db_column='pro_id')
    com_descripcion = models.CharField(max_length=100, null=False, db_column='com_descripcion')
    com_vigente = models.BooleanField(default=True, null=False, db_column='com_vigente')

    class Meta:
        db_table = 'comuna'

class Alimentacion(models.Model):
    ali_id = models.BigAutoField(primary_key=True, db_column='ali_id')
    ali_descripcion = models.CharField(max_length=100, null=True, db_column='ali_descripcion')
    ali_tipo_opcion = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    ali_tipo = models.IntegerField(choices=ali_tipo_opcion, null=True, db_column='ali_tipo')
    ali_vigente = models.BooleanField(default=True, null=True, db_column='ali_vigente')

    class Meta:
        db_table = 'alimentacion'

class Concepto_Contable(models.Model):
    coc_id = models.BigAutoField(primary_key=True, db_column='coc_id')
    coc_descripcion = models.CharField(max_length=50, null=False, db_column='coc_descripcion')
    coc_vigente = models.BooleanField(default=True, null=False, db_column='coc_vigente')

    class Meta:
        db_table = 'concepto_contable'

class Tipo_Curso(models.Model):
    tcu_id = models.BigAutoField(primary_key=True, db_column='tcu_id')
    tcu_descripcion = models.CharField(max_length=100, null=False, db_column='tcu_descripcion')
    tcu_tipo_opcion = [
        (1, 'Inicial'),
        (2, 'Medio'),
        (3, 'Avanzado'),
        (4, 'Habilitación'),
        (5, 'Verificación'),
        (6, 'Institucional'),
    ]
    tcu_tipo = models.IntegerField(choices=tcu_tipo_opcion, null=False, db_column='tcu_tipo')
    tcu_cant_participante = models.IntegerField(null=True, db_column='tcu_cant_participante')
    tcu_vigente = models.BooleanField(default=True, null=False, db_column='tcu_vigente')

    class Meta:
        db_table = 'tipo_curso'

class Tipo_Archivo(models.Model):
    tar_id = models.BigAutoField(primary_key=True, db_column='tar_id')
    tar_descripcion = models.CharField(max_length=50, null=False, db_column='tar_descripcion')
    tar_vigente = models.BooleanField(default=True, null=False, db_column='tar_vigente')

    class Meta:
        db_table = 'tipo_archivo'