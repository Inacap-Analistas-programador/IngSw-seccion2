from django.db import models

class Rol(models.Model):
    ROL_ID = models.BigAutoField(primary_key=True)
    ROL_DESCRIPCION = models.CharField(max_length=50, null=False)
    ROL_TIPO = models.IntegerField(null=False)
    ROL_VIGENTE = models.BooleanField(default=True, null=False)

class Cargo(models.Model):
    CAR_ID = models.BigAutoField(primary_key=True)
    CAR_DESCRIPCION = models.CharField(max_length=100, null=False)
    CAR_VIGENTE = models.BooleanField(default=True, null=False)

class Rama(models.Model):
    RAM_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    RAM_DESCRIPCION = models.CharField(max_length=50)
    RAM_VIGENTE = models.BooleanField(default=True)

class Estado_Civil(models.Model):
    ESC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ESC_DESCRIPCION = models.CharField(max_length=50)
    ESC_VIGENTE = models.BooleanField(default=True)

class Nivel(models.Model):
    NIV_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    NIV_DESCRIPCION = models.CharField(max_length=100)
    NIV_ORDEN = models.IntegerField()
    NIV_VIGENTE = models.BooleanField(default=True)

class Zona(models.Model):
    ZON_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ZON_DESCRIPCION = models.CharField(max_length=100)
    ZON_UNILATERAL = models.BooleanField(default=False)
    ZON_VIGENTE = models.BooleanField(default=True)

class Distrito(models.Model):
    DIS_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ZON_ID = models.ForeignKey('Zona', on_delete=models.CASCADE)
    DIS_DESCRIPCION = models.CharField(max_length=100)
    DIS_VIGENTE = models.BooleanField(default=True)

class Grupo(models.Model):
    GRU_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    DIS_ID = models.ForeignKey('Distrito', on_delete=models.CASCADE)
    GRU_DESCRIPCION = models.CharField(max_length=100)
    GRU_VIGENTE = models.BooleanField(default=True)

class Region(models.Model):
    REG_ID = models.BigAutoField(primary_key=True)
    REG_DESCRIPCION = models.CharField(max_length=100, null=False)
    REG_VIGENTE = models.BooleanField(default=True, null=False)

class Provincia(models.Model):
    PRO_ID = models.BigAutoField(primary_key=True)
    REG_ID = models.ForeignKey('Region',on_delete=models.PROTECT, null=False)
    PRO_DESCRIPCION = models.CharField(max_length=100, null=False)
    PRO_VIGENTE = models.BooleanField(default=True, null=False)

class Comuna(models.Model):
    COM_ID = models.BigAutoField(primary_key=True)
    PRO_ID = models.ForeignKey('Provincia',on_delete=models.PROTECT, null=False)
    COM_DESCRIPCION = models.CharField(max_length=100, null=False)
    COM_VIGENTE = models.BooleanField(default=True, null=False)

class Alimentacion(models.Model):
    ALI_ID = models.BigAutoField(primary_key=True)
    ALI_DESCRIPCION = models.CharField(max_length=100, null=False)
    ALI_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    ALI_TIPO = models.IntegerField(choices=ALI_TIPO_OPCION, null=False)
    ALI_VIGENTE = models.BooleanField(default=True, null=False)
