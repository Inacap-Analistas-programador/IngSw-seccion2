from django.db import models

class Archivo(models.Model):
    ARC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    TAR_ID = models.ForeignKey('Tipo_Archivo', on_delete=models.CASCADE)
    USU_ID_CREA = models.ForeignKey('ModuloUsuarios.Usuario', on_delete=models.CASCADE, related_name='usuario_crea')
    USU_ID_MODIFICA = models.ForeignKey('ModuloUsuarios.Usuario', on_delete=models.CASCADE, related_name='usuario_modifica', blank=True, null=True)
    ARC_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    ARC_DESCRIPCION = models.CharField(max_length=100)
    ARC_RUTA = models.CharField()
    ARC_VIGENTE = models.BooleanField(default=True)

class Archivo_Curso(models.Model):
    ARU_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('ModuloCursos.Curso', on_delete=models.CASCADE)

class Archivo_Persona(models.Model):
    ARP_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('ModuloUsuarios.Persona', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('ModuloCursos.Curso', on_delete=models.CASCADE, blank=True, null=True)

class Tipo_Archivo(models.Model):
    TAR_ID = models.BigAutoField(primary_key=True)
    TAR_DESCRIPCION = models.CharField(max_length=50, null=False)
    TAR_VIGENTE = models.BooleanField(default=True, null=False)

