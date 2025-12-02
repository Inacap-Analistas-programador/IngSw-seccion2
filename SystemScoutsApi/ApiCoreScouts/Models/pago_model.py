from django.db import models
from .persona_model import *
from .curso_model import *
from .mantenedor_model import *

class Proveedor(models.Model):
    PRV_ID = models.BigAutoField(primary_key=True, db_column='prv_id')
    PRV_DESCRIPCION = models.CharField(max_length=100, null=False, db_column='prv_descripcion')
    PRV_CELULAR1 = models.CharField(max_length=15, blank=True, null=False, db_column='prv_celular1')
    PRV_CELULAR2 = models.CharField(max_length=15, blank=True, null=True, db_column='prv_celular2')
    PRV_DIRECCION = models.CharField(max_length=100, blank=True, null=False, db_column='prv_direccion')
    PRV_OBSERVACION = models.CharField(max_length=500, blank=True, null=True, db_column='prv_observacion')
    PRV_VIGENTE = models.BooleanField(default=True, null=False, db_column='prv_vigente')

    class Meta:
        db_table = 'proveedor'

class Comprobante_Pago(models.Model):
    CPA_ID = models.BigAutoField(primary_key=True, db_column='cpa_id')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='usu_id')
    PEC_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='pec_id')
    COC_ID = models.ForeignKey(Concepto_Contable, on_delete=models.PROTECT, null=False, db_column='coc_id')
    CPA_FECHA_HORA = models.DateTimeField(null=False, db_column='cpa_fecha_hora')
    CPA_FECHA = models.DateField(auto_now_add=True, null=False, db_column='cpa_fecha')
    CPA_NUMERO = models.IntegerField(null=False, db_column='cpa_numero')
    CPA_VALOR = models.DecimalField(max_digits=21, decimal_places=2, null=False, db_column='cpa_valor')

    class Meta:
        db_table = 'comprobante_pago'

class Pago_Comprobante(models.Model):
    PCO_ID = models.BigAutoField(primary_key=True, db_column='pco_id')
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=False, db_column='pap_id')
    CPA_ID = models.ForeignKey('Comprobante_Pago', on_delete=models.PROTECT, null=False, db_column='cpa_id')

    class Meta:
        db_table = 'pago_comprobante'

class Pago_Persona(models.Model):
    PAP_ID = models.BigAutoField(primary_key=True, db_column='pap_id')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    CUR_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='cur_id')
    USU_ID = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, db_column='usu_id')
    PAP_FECHA_HORA = models.DateTimeField(null=False, db_column='pap_fecha_hora')
    PAP_TIPO_OPCION = [
        (1, 'Ingreso'),
        (2, 'Egreso'),
    ]
    PAP_TIPO = models.IntegerField(choices=PAP_TIPO_OPCION, null=True, db_column='pap_tipo')
    PAP_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='pap_valor')
    PAP_ESTADO_OPCION = [
        (1,'Pagado'),
        (2, 'Anulado')
    ]
    PAP_ESTADO = models.IntegerField(choices=PAP_ESTADO_OPCION, null=False, db_column='pap_estado')
    PAP_OBSERVACION = models.CharField(max_length=500, null=True, db_column='pap_observacion')

    class Meta:
        db_table = 'pago_persona'

class Prepago(models.Model):
    PPA_ID = models.BigAutoField(primary_key=True, db_column='ppa_id')
    PER_ID = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, db_column='per_id')
    CUR_ID = models.ForeignKey(Curso, on_delete=models.PROTECT, null=False, db_column='cur_id')
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=True, db_column='pap_id')
    PPA_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False, db_column='ppa_valor')
    PPA_OBSERVACION = models.CharField(max_length=500, null=True, db_column='ppa_observacion')
    PPA_VIGENTE = models.BooleanField(default=True, null=False, db_column='ppa_vigente')

    class Meta:
        db_table = 'prepago'