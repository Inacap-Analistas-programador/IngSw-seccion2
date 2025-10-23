from django.db import models

class Archivo(models.Model):
    ARC_ID = models.BigAutoField(primary_key=True)
    TAR_ID = models.ForeignKey('Tipo_Archivo', on_delete=models.PROTECT, null=False)
    USU_ID_CREA = models.ForeignKey('ModuloUsuarioCurso.Usuario', on_delete=models.PROTECT, related_name='usuario_crea', null=False)
    USU_ID_MODIFICA = models.ForeignKey('ModuloUsuarioCurso.Usuario', on_delete=models.PROTECT, related_name='usuario_modifica', null=True)
    ARC_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False)
    ARC_DESCRIPCION = models.CharField(max_length=100, null=False)
    ARC_RUTA = models.CharField(max_length=255, null=False)
    ARC_VIGENTE = models.BooleanField(default=True, null=False)

class Archivo_Curso(models.Model):
    ARU_ID = models.BigAutoField(primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False)
    CUS_ID = models.ForeignKey('ModuloUsuarioCurso.Curso', on_delete=models.PROTECT, null=False)

class Archivo_Persona(models.Model):
    ARP_ID = models.BigAutoField(primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey('ModuloUsuarioCurso.Persona', on_delete=models.PROTECT, null=False)
    CUS_ID = models.ForeignKey('ModuloUsuarioCurso.Curso', on_delete=models.CASCADE, null=True)

class Tipo_Archivo(models.Model):
    TAR_ID = models.BigAutoField(primary_key=True)
    TAR_DESCRIPCION = models.CharField(max_length=50, null=False)
    TAR_VIGENTE = models.BooleanField(default=True, null=False)

