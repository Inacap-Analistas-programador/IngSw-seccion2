from django.db import models

class Rol(models.Model):
    ROL_ID = models.BigAutoField(primary_key=True, db_column='rol_id')
    ROL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='rol_descripcion')
    ROL_TIPO_OPTIONS = [
        (1, 'Participante'),
        (2, 'Formadores'),
        (3, 'Apoyo Formadores'),
        (4, 'Organización'),
        (5, 'Servicio'),
        (6, 'Salud'),
    ]
    ROL_TIPO = models.IntegerField(choices=ROL_TIPO_OPTIONS, null=False, db_column='rol_tipo')
    ROL_VIGENTE = models.BooleanField(default=True, null=False, db_column='rol_vigente')

    class Meta:
        db_table = 'rol'

class Cargo(models.Model):
    CAR_ID = models.BigAutoField(primary_key=True, db_column='car_id')
    CAR_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='car_descripcion')
    CAR_VIGENTE = models.BooleanField(default=True, null=False, db_column='car_vigente')

    class Meta:
        db_table = 'cargo'

class Rama(models.Model):
    RAM_ID = models.BigAutoField(primary_key=True, db_column='ram_id')
    RAM_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='ram_descripcion')
    RAM_VIGENTE = models.BooleanField(default=True, null=False, db_column='ram_vigente')

    class Meta:
        db_table = 'rama'

class Estado_Civil(models.Model):
    ESC_ID = models.BigAutoField(primary_key=True, db_column='esc_id')
    ESC_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='esc_descripcion')
    ESC_VIGENTE = models.BooleanField(default=True, null=False, db_column='esc_vigente')

    class Meta:
        db_table = 'estado_civil'

class Nivel(models.Model):
    NIV_ID = models.BigAutoField(primary_key=True, db_column='niv_id')
    NIV_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='niv_descripcion')
    NIV_ORDEN = models.IntegerField(null=False, db_column='niv_orden')
    NIV_VIGENTE = models.BooleanField(default=True, null=False, db_column='niv_vigente')

    class Meta:
        db_table = 'nivel'

class Zona(models.Model):
    ZON_ID = models.BigAutoField(primary_key=True, db_column='zon_id')
    ZON_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='zon_descripcion')
    ZON_UNILATERAL = models.BooleanField(default=False, null=False, db_column='zon_unilateral')
    ZON_VIGENTE = models.BooleanField(default=True, null=False, db_column='zon_vigente')

    class Meta:
        db_table = 'zona'

class Distrito(models.Model):
    DIS_ID = models.BigAutoField(primary_key=True, db_column='dis_id')
    ZON_ID = models.ForeignKey('Zona', on_delete=models.PROTECT, null=False, db_column='zon_id')
    DIS_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='dis_descripcion')
    DIS_VIGENTE = models.BooleanField(default=True, null=False, db_column='dis_vigente')

    class Meta:
        db_table = 'distrito'

class Grupo(models.Model):
    GRU_ID = models.BigAutoField(primary_key=True, db_column='gru_id')
    DIS_ID = models.ForeignKey('Distrito', on_delete=models.PROTECT, null=False, db_column='dis_id')
    GRU_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='gru_descripcion')
    GRU_VIGENTE = models.BooleanField(default=True, null=False, db_column='gru_vigente')

    class Meta:
        db_table = 'grupo'

class Region(models.Model):
    REG_ID = models.BigAutoField(primary_key=True, db_column='reg_id')
    REG_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='reg_descripcion')
    REG_VIGENTE = models.BooleanField(default=True, null=False, db_column='reg_vigente')

    class Meta:
        db_table = 'region'

class Provincia(models.Model):
    PRO_ID = models.BigAutoField(primary_key=True, db_column='pro_id')
    REG_ID = models.ForeignKey('Region',on_delete=models.PROTECT, null=False, db_column='reg_id')
    PRO_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='pro_descripcion')
    PRO_VIGENTE = models.BooleanField(default=True, null=False, db_column='pro_vigente')

    class Meta:
        db_table = 'provincia'

class Comuna(models.Model):
    COM_ID = models.BigAutoField(primary_key=True, db_column='com_id')
    PRO_ID = models.ForeignKey('Provincia',on_delete=models.PROTECT, null=False, db_column='pro_id')
    COM_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='com_descripcion')
    COM_VIGENTE = models.BooleanField(default=True, null=False, db_column='com_vigente')

    class Meta:
        db_table = 'comuna'

class Alimentacion(models.Model):
    ALI_ID = models.BigAutoField(primary_key=True, db_column='ali_id')
    ALI_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='ali_descripcion')
    ALI_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    ALI_TIPO = models.IntegerField(choices=ALI_TIPO_OPCION, null=False, db_column='ali_tipo')
    ALI_VIGENTE = models.BooleanField(default=True, null=False, db_column='ali_vigente')

    class Meta:
        db_table = 'alimentacion'

class Concepto_Contable(models.Model):
    COC_ID = models.BigAutoField(primary_key=True, db_column='coc_id')
    COC_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='coc_descripcion')
    COC_VIGENTE = models.BooleanField(default=True, null=False, db_column='coc_vigente')

    class Meta:
        db_table = 'concepto_contable'

class Tipo_Curso(models.Model):
    TCU_ID = models.BigAutoField(primary_key=True, db_column='tcu_id')
    TCU_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='tcu_descripcion')
    TCU_TIPO_OPCION = [
        (1, 'Inicial'),
        (2, 'Medio'),
        (3, 'Avanzado'),
        (4, 'Habilitación'),
        (5, 'Verificación'),
        (6, 'Institucional'),
    ]
    TCU_TIPO = models.IntegerField(choices=TCU_TIPO_OPCION, null=False, db_column='tcu_tipo')
    TCU_CANT_PARTICIPANTE = models.IntegerField(null=True, db_column='tcu_cant_participante')
    TCU_VIGENTE = models.BooleanField(default=True, null=False, db_column='tcu_vigente')

    class Meta:
        db_table = 'tipo_curso'

class Tipo_Archivo(models.Model):
    TAR_ID = models.BigAutoField(primary_key=True, db_column='tar_id')
    TAR_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='tar_descripcion')
    TAR_VIGENTE = models.BooleanField(default=True, null=False, db_column='tar_vigente')

    class Meta:
        db_table = 'tipo_archivo'