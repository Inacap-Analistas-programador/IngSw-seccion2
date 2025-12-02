from django.db import models
from .persona_model import *
from .curso_model import *
from .mantenedor_model import *

class Proveedor(models.Model):
    prv_id = models.BigAutoField(primary_key=True, db_column='prv_id')
    prv_descripcion = models.CharField(max_length=100, null=False, db_column='prv_descripcion')
    prv_celular1 = models.CharField(max_length=15, blank=True, null=False, db_column='prv_celular1')
    prv_celular2 = models.CharField(max_length=15, blank=True, null=True, db_column='prv_celular2')
    prv_direccion = models.CharField(max_length=100, blank=True, null=False, db_column='prv_direccion')
    prv_observacion = models.CharField(max_length=500, blank=True, null=True, db_column='prv_observacion')
    prv_vigente = models.BooleanField(default=True, null=False, db_column='prv_vigente')

    class Meta:
        db_table = 'proveedor'

class Comprobante_Pago(models.Model):
    cpa_id = models.BigAutoField(primary_key=True, db_column='cpa_id')
    usu_id = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='usu_id')
    pec_id = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='pec_id')
    coc_id = models.ForeignKey(Concepto_Contable, on_delete=models.PROTECT, null=False, db_column='coc_id')
    cpa_fecha_hora = models.DateTimeField(null=False, db_column='cpa_fecha_hora')
    cpa_fecha = models.DateField(auto_now_add=True, null=False, db_column='cpa_fecha')
    cpa_numero = models.IntegerField(null=False, db_column='cpa_numero')
    cpa_valor = models.DecimalField(max_digits=21, decimal_places=2, null=False, db_column='cpa_valor')

    class Meta:
        db_table = 'comprobante_pago'

class Pago_Comprobante(models.Model):
    pco_id = models.BigAutoField(primary_key=True, db_column='pco_id')
    pap_id = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=False, db_column='pap_id')
    cpa_id = models.ForeignKey('Comprobante_Pago', on_delete=models.PROTECT, null=False, db_column='cpa_id')

    class Meta:
        db_table = 'pago_comprobante'

class Pago_Persona(models.Model):
    pap_id = models.BigAutoField(primary_key=True, db_column='pap_id')
    per_id = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    cur_id = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='cur_id')
    usu_id = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='usu_id')
    pap_fecha_hora = models.DateTimeField(null=False, db_column='pap_fecha_hora')
    pap_tipo_opcion = [
        (1, 'Ingreso'),
        (2, 'Egreso'),
    ]
    pap_tipo = models.IntegerField(choices=pap_tipo_opcion, null=True, db_column='pap_tipo')
    pap_valor = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='pap_valor')
    pap_estado_opcion = [
        (1,'Pagado'),
        (2, 'Anulado')
    ]
    pap_estado = models.IntegerField(choices=pap_estado_opcion, null=False, db_column='pap_estado')
    pap_observacion = models.CharField(max_length=500, null=True, db_column='pap_observacion')

    class Meta:
        db_table = 'pago_persona'

class Prepago(models.Model):
    ppa_id = models.BigAutoField(primary_key=True, db_column='ppa_id')
    per_id = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    cur_id = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='cur_id')
    pap_id = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=True, db_column='pap_id')
    ppa_valor = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='ppa_valor')
    ppa_observacion = models.CharField(max_length=500, null=True, db_column='ppa_observacion')
    ppa_vigente = models.BooleanField(default=True, null=False, db_column='ppa_vigente')

    class Meta:
        db_table = 'prepago'