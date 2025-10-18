from django.db import models

class Concepto_Contable(models.Model):
    COC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    COC_DESCRIPCION = models.CharField(max_length=100)
    COC_VIGENTE = models.BooleanField(default=True)

class Proveedor(models.Model):
    PRV_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PRV_DESCRIPCION = models.CharField(max_length=100)
    PRV_CELULAR1 = models.CharField(max_length=15, blank=True, null=True)
    PRV_CELULAR2 = models.CharField(max_length=15, blank=True, null=True)
    PRV_DIRECCION = models.CharField(max_length=100, blank=True, null=True)
    PRV_OBSERVACION = models.CharField(blank=True, null=True)
    PRV_VIGENTE = models.BooleanField(default=True)
