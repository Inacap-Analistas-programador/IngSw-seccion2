from django.db import models

class Rol(models.Model):
    ROL_ID = models.BigAutoField(primary_key=True,db_column='ROL_ID')
    ROL_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='ROL_DESCRIPCION')
    ROL_TIPO_OPTIONS = [
        (1, 'Participante'),
        (2, 'Formadores'),
        (3, 'Apoyo Formadores'),
        (4, 'Organización'),
        (5, 'Servicio'),
        (6, 'Salud'),
    ]
    ROL_TIPO = models.IntegerField(choices=ROL_TIPO_OPTIONS, null=False, db_column='ROL_TIPO')
    ROL_VIGENTE = models.BooleanField(default=True, null=False, db_column='ROL_VIGENTE')

    class Meta:
        db_table = 'ROL'

class Cargo(models.Model):
    CAR_ID = models.BigAutoField(primary_key=True, db_column='CAR_ID')
    CAR_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='CAR_DESCRIPCION')
    CAR_VIGENTE = models.BooleanField(default=True, null=False, db_column='CAR_VIGENTE')

    class Meta:
        db_table = 'CARGO'

class Rama(models.Model):
    RAM_ID = models.BigAutoField(primary_key=True, db_column='RAM_ID')
    RAM_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='RAM_DESCRIPCION')
    RAM_VIGENTE = models.BooleanField(default=True, null=False, db_column='RAM_VIGENTE')

    class Meta:
        db_table = 'RAMA'

class Estado_Civil(models.Model):
    ESC_ID = models.BigAutoField(primary_key=True, db_column='ESC_ID')
    ESC_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='ESC_DESCRIPCION')
    ESC_VIGENTE = models.BooleanField(default=True, null=False, db_column='ESC_VIGENTE')

    class Meta:
        db_table = 'ESTADO_CIVIL'

class Nivel(models.Model):
    NIV_ID = models.BigAutoField(primary_key=True, db_column='NIV_ID')
    NIV_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='NIV_DESCRIPCION')
    NIV_ORDEN = models.IntegerField(null=False, db_column='NIV_ORDEN')
    NIV_VIGENTE = models.BooleanField(default=True, null=False, db_column='NIV_VIGENTE')

    class Meta:
        db_table = 'NIVEL'

class Zona(models.Model):
    ZON_ID = models.BigAutoField(primary_key=True, db_column='ZON_ID')
    ZON_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='ZON_DESCRIPCION')
    ZON_UNILATERAL = models.BooleanField(default=False, null=False, db_column='ZON_UNILATERAL')
    ZON_VIGENTE = models.BooleanField(default=True, null=False, db_column='ZON_VIGENTE')

    class Meta:
        db_table = 'ZONA'

class Distrito(models.Model):
    DIS_ID = models.BigAutoField(primary_key=True, db_column='DIS_ID')
    ZON_ID = models.ForeignKey('Zona', on_delete=models.PROTECT, null=False, db_column='ZON_ID')
    DIS_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='DIS_DESCRIPCION')
    DIS_VIGENTE = models.BooleanField(default=True, null=False, db_column='DIS_VIGENTE')

    class Meta:
        db_table = 'DISTRITO'

class Grupo(models.Model):
    GRU_ID = models.BigAutoField(primary_key=True, db_column='GRU_ID')
    DIS_ID = models.ForeignKey('Distrito', on_delete=models.PROTECT, null=False, db_column='DIS_ID')
    GRU_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='GRU_DESCRIPCION')
    GRU_VIGENTE = models.BooleanField(default=True, null=False, db_column='GRU_VIGENTE')

    class Meta:
        db_table = 'GRUPO'

class Region(models.Model):
    REG_ID = models.BigAutoField(primary_key=True, db_column='REG_ID')
    REG_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='REG_DESCRIPCION')
    REG_VIGENTE = models.BooleanField(default=True, null=False, db_column='REG_VIGENTE')

    class Meta:
        db_table = 'REGION'

class Provincia(models.Model):
    PRO_ID = models.BigAutoField(primary_key=True, db_column='PRO_ID')
    REG_ID = models.ForeignKey('Region',on_delete=models.PROTECT, null=False, db_column='REG_ID')
    PRO_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='PRO_DESCRIPCION')
    PRO_VIGENTE = models.BooleanField(default=True, null=False, db_column='PRO_VIGENTE')

    class Meta:
        db_table = 'PROVINCIA'

class Comuna(models.Model):
    COM_ID = models.BigAutoField(primary_key=True, db_column='COM_ID')
    PRO_ID = models.ForeignKey('Provincia',on_delete=models.PROTECT, null=False, db_column='PRO_ID')
    COM_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='COM_DESCRIPCION')
    COM_VIGENTE = models.BooleanField(default=True, null=False, db_column='COM_VIGENTE')

    class Meta:
        db_table = 'COMUNA'

class Alimentacion(models.Model):
    ALI_ID = models.BigAutoField(primary_key=True, db_column='ALI_ID')
    ALI_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='ALI_DESCRIPCION')
    ALI_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    ALI_TIPO = models.IntegerField(choices=ALI_TIPO_OPCION, null=False, db_column='ALI_TIPO')
    ALI_VIGENTE = models.BooleanField(default=True, null=False, db_column='ALI_VIGENTE')

    class Meta:
        db_table = 'ALIMENTACION'

class Concepto_Contable(models.Model):
    COC_ID = models.BigAutoField(primary_key=True, db_column='COC_ID')
    COC_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='COC_DESCRIPCION')
    COC_VIGENTE = models.BooleanField(default=True, null=False, db_column='COC_VIGENTE')

    class Meta:
        db_table = 'CONCEPTO_CONTABLE'

class Tipo_Curso(models.Model):
    TCU_ID = models.BigAutoField(primary_key=True, db_column='TCU_ID')
    TCU_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='TCU_DESCRIPCION')
    TCU_TIPO_OPCION = [
        (1, 'Inicial'),
        (2, 'Medio'),
        (3, 'Avanzado'),
        (4, 'Habilitación'),
        (5, 'Verificación'),
        (6, 'Institucional'),
    ]
    TCU_TIPO = models.IntegerField(choices=TCU_TIPO_OPCION, null=False, db_column='TCU_TIPO')
    TCU_CANT_PARTICIPANTE = models.IntegerField(null=True, db_column='TCU_CANT_PARTICIPANTE')
    TCU_VIGENTE = models.BooleanField(default=True, null=False, db_column='TCU_VIGENTE')

    class Meta:
        db_table = 'TIPO_CURSO'

class Tipo_Archivo(models.Model):
    TAR_ID = models.BigAutoField(primary_key=True, db_column='TAR_ID')
    TAR_DESCRIPCION = models.CharField(max_length=50, null=False, db_column='TAR_DESCRIPCION')
    TAR_VIGENTE = models.BooleanField(default=True, null=False, db_column='TAR_VIGENTE')

    class Meta:
        db_table = 'TIPO_ARCHIVO'