from django.db import models

class Concepto_Contable(models.Model):
    COC_ID = models.BigAutoField(primary_key=True)
    COC_DESCRIPCION = models.CharField(max_length=50, null=False)
    COC_VIGENTE = models.BooleanField(default=True, null=False)

class Proveedor(models.Model):
    PRV_ID = models.BigAutoField(primary_key=True)
    PRV_DESCRIPCION = models.CharField(max_length=100, null=False)
    PRV_CELULAR1 = models.CharField(max_length=15, blank=True, null=False)
    PRV_CELULAR2 = models.CharField(max_length=15, blank=True, null=True)
    PRV_DIRECCION = models.CharField(max_length=100, blank=True, null=False)
    PRV_OBSERVACION = models.CharField(max_length=500, blank=True, null=True)
    PRV_VIGENTE = models.BooleanField(default=True, null=False)

class Comprobante_Pago(models.Model):
    CPA_ID = models.BigAutoField(primary_key=True)
    USU_ID = models.ForeignKey('ModuloUsuarioCurso.Usuario', on_delete=models.PROTECT, null=False)
    PEC_ID = models.ForeignKey('ModuloUsuarioCurso.Persona_Curso', on_delete=models.PROTECT, null=False)
    COC_ID = models.ForeignKey('Concepto_Contable', on_delete=models.PROTECT, null=False)
    CPA_FECHA_HORA = models.DateTimeField(null=False)
    CPA_FECHA = models.DateField(auto_now_add=True, null=False)
    CPA_NUMERO = models.IntegerField(null=False)
    CPA_VALOR = models.DecimalField(max_digits=21, decimal_places=2, null=False)

class Pago_Comprobante(models.Model):
    PCO_ID = models.BigAutoField(primary_key=True)
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=False)
    CPA_ID = models.ForeignKey('Comprobante_Pago', on_delete=models.PROTECT, null=False)

class Pago_Persona(models.Model):
    PAP_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('ModuloUsuarioCurso.Persona', on_delete=models.PROTECT, null=False)
    CUR_ID = models.ForeignKey('ModuloUsuarioCurso.Curso', on_delete=models.PROTECT, null=False)
    USU_ID = models.ForeignKey('ModuloUsuarioCurso.Usuario', on_delete=models.PROTECT, null=False)
    PAP_FECHA_HORA = models.DateTimeField(null=False)
    PAP_TIPO_OPCION = [
        (1, 'Ingreso'),
        (2, 'Egreso'),
    ]
    PAP_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False)
    PAP_OBSERVACION = models.CharField(max_length=500, null=True)

class Prepago(models.Model):
    PPA_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('ModuloUsuarioCurso.Persona', on_delete=models.PROTECT, null=False)
    CUR_ID = models.ForeignKey('ModuloUsuarioCurso.Curso', on_delete=models.PROTECT, null=False)
    PAP_ID = models.ForeignKey('Pago_Persona', on_delete=models.PROTECT, null=True)
    PPA_VALOR = models.DecimalField(max_digits=21, decimal_places=6, null=False)
    PPA_OBSERVACION = models.CharField(max_length=500, null=True)
    PPA_VIGENTE = models.BooleanField(default=True, null=False)