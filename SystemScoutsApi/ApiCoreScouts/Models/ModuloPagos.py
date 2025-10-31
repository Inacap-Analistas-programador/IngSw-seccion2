from django.db import models
from .ModuloPersonas import *
from .ModuloCursos import *
from .ModuloMantenedores import *

class Proveedor(models.Model):
    PRV_ID = models.BigAutoField(primary_key=True, db_column='PRV_ID')
    PRV_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='PRV_DESCRIPCION')
    PRV_CELULAR1 = models.CharField(max_length=15, blank=True, null=False, db_column='PRV_CELULAR1')
    PRV_CELULAR2 = models.CharField(max_length=15, blank=True, null=True, db_column='PRV_CELULAR2')
    PRV_DIRECCION = models.CharField(max_length=100, blank=True, null=False, db_column='PRV_DIRECCION')
    PRV_OBSERVACION = models.CharField(max_length=500, blank=True, null=True, db_column='PRV_OBSERVACION')
    PRV_VIGENTE = models.BooleanField(default=True, null=False, db_column='PRV_VIGENTE')

    class Meta:
        db_table = 'PROVEEDOR'

class Comprobante_Pago(models.Model):
    CPA_ID = models.BigAutoField(primary_key=True, db_column='CPA_ID')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='USU_ID')
    PEC_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='PEC_ID')
    COC_ID = models.ForeignKey(Concepto_Contable, on_delete=models.PROTECT, null=False, db_column='COC_ID')
    CPA_FECHA_HORA = models.DateTimeField(null=False, db_column='CPA_FECHA_HORA')
    CPA_FECHA = models.DateField(auto_now_add=True, null=False, db_column='CPA_FECHA')
    CPA_NUMERO = models.IntegerField(null=False, db_column='CPA_NUMERO')
    CPA_VALOR = models.DecimalField(max_digits=21, decimal_places=2, null=False, db_column='CPA_VALOR')

    class Meta:
        db_table = 'COMPROBANTE_PAGO'

class Pago_Comprobante(models.Model):
    PCO_ID = models.BigAutoField(primary_key=True, db_column='PCO_ID')
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=False, db_column='PAP_ID')
    CPA_ID = models.ForeignKey('Comprobante_Pago', on_delete=models.PROTECT, null=False, db_column='CPA_ID')

    class Meta:
        db_table = 'PAGO_COMPROBANTE'

class Pago_Persona(models.Model):
    PAP_ID = models.BigAutoField(primary_key=True, db_column='PAP_ID')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CUR_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='USU_ID')
    PAP_FECHA_HORA = models.DateTimeField(null=False, db_column='PAP_FECHA_HORA')
    PAP_TIPO_OPCION = [
        (1, 'Ingreso'),
        (2, 'Egreso'),
    ]
    PAP_TIPO = models.IntegerField(choices=PAP_TIPO_OPCION, null=True, db_column='PAP_TIPO')
    PAP_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='PAP_VALOR')
    PAP_ESTADO_OPCION = [
        (1,'Pagado'),
        (2, 'Anulado')
    ]
    PAP_ESTADO = models.IntegerField(choices=PAP_ESTADO_OPCION, null=False, db_column='PAP_ESTADO')
    PAP_OBSERVACION = models.CharField(max_length=500, null=True, db_column='PAP_OBSERVACION')

    class Meta:
        db_table = 'PAGO_PERSONA'

class Prepago(models.Model):
    PPA_ID = models.BigAutoField(primary_key=True, db_column='PPA_ID')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='PER_ID')
    CUR_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='CUR_ID')
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=True, db_column='PAP_ID')
    PPA_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='PPA_VALOR')
    PPA_OBSERVACION = models.CharField(max_length=500, null=True, db_column='PPA_OBSERVACION')
    PPA_VIGENTE = models.BooleanField(default=True, null=False, db_column='PPA_VIGENTE')

    class Meta:
        db_table = 'PREPAGO'