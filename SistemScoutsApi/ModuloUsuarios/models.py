from django.db import models

class Perfil(models.Model):
    PEL_ID = models.BigAutoField(primary_key=True)
    PEL_DESCRIPCION = models.CharField(max_length=50, null=False)
    PEL_VIGENTE = models.BooleanField(default=True, null=False)

class Usuario(models.Model):
    USU_ID = models.BigAutoField(primary_key=True)
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False)
    USU_USERNAME = models.CharField(max_length=100, unique=True, null=False)
    USU_PASSWORD = models.CharField(max_length=50, null=False)  
    USU_RUTA_FOTO = models.CharField(max_length=255, null=False)
    USU_VIGENTE = models.BooleanField(default=True, null=False)

class Aplicacion(models.Model):
    APL_ID = models.BigAutoField(primary_key=True)
    APL_DESCRIPCION = models.CharField(max_length=50, null=False)
    APL_VIGENTE = models.BooleanField(default=True, null=False)

class Persona(models.Model):
    PER_ID = models.BigAutoField(primary_key=True)
    ESC_ID = models.ForeignKey('ModuloMantenedores.Estado_Civil', on_delete=models.PROTECT, null=False)
    COM_ID = models.ForeignKey('ModuloMantenedores.Comuna', on_delete=models.PROTECT, null=False)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False)
    PER_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False)
    PER_RUN = models.CharField(max_length=9, unique=True, null=False)
    PER_DV = models.CharField(max_length=1, null=False)
    PER_APELPTA = models.CharField(max_length=50, null=False)
    PER_APELMAT = models.CharField(max_length=50, null=True)
    PER_NOMBRES = models.CharField(max_length=50, null=False)
    PER_MAIL = models.CharField(max_length=100, null=False)
    PER_FECHA_NAC = models.DateField()
    PER_DIRECCION = models.CharField(max_length=255)
    PER_TIPO_FONO_OPTIONS = [
        (1, 'Fono Fijo'),
        (2, 'Celular'),
        (3, 'Celular/WhatsApp'),
        (4, 'WhatsApp'),
    ]
    PER_TIPO_FONO = models.IntegerField(choices=PER_TIPO_FONO_OPTIONS, null=False)
    PER_FONO = models.CharField(max_length=15, blank=True, null=False)
    PER_ALERGIA_ENFERMEDAD = models.CharField(max_length=255, null=True)
    PER_LIMITACION = models.CharField(max_length=255, null=True)
    PER_NOM_EMERGENCIA = models.CharField(max_length=50, null=True)
    PER_FONO_EMERGENCIA = models.CharField(max_length=15, null=True)
    PER_OTROS = models.CharField(max_length=255, null=True)
    PER_NUM_MMA = models.IntegerField(null=True)
    PER_PROFESION = models.CharField(max_length=100, null=True)
    PER_TIEMPO_NNAJ = models.CharField(max_length=100, null=True)
    PER_TIEMPO_ADULTO = models.CharField(max_length=100, null=True)
    PER_RELIGION = models.CharField(max_length=100, null=True)
    PER_APODO = models.CharField(max_length=50, null=False)
    PER_FOTO = models.CharField(max_length=255, null=True)
    PER_VIGENTE = models.BooleanField(default=True, null=False)

class Persona_Grupo(models.Model):
    PEG_ID = models.BigAutoField(primary_key=True)
    GRU_ID = models.ForeignKey('ModuloMantenedores.Grupo', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    PEG_VIGENTE = models.BooleanField(default=True, null=False)

class Persona_Formador(models.Model):
    PEF_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    PEF_HAB_1 = models.BooleanField(default=False, null=False)
    PEF_HAB_2 = models.BooleanField(default=False, null=False)
    PEF_VERIF = models.BooleanField(default=False, null=False)
    PEF_HISTORIAL = models.CharField(blank=True, null=True)

class Persona_Individual(models.Model):
    PEI_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    CAR_ID = models.ForeignKey('ModuloMantenedores.Cargo', on_delete=models.PROTECT, null=False)
    DIS_ID = models.ForeignKey('ModuloMantenedores.Distrito', on_delete=models.PROTECT, null=True)
    ZON_ID = models.ForeignKey('ModuloMantenedores.Zona', on_delete=models.PROTECT, null=True)
    PEI_VIGENTE = models.BooleanField(default=True, null=False)

class Persona_Nivel(models.Model):
    PEN_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    NIV_ID = models.ForeignKey('ModuloMantenedores.Nivel', on_delete=models.PROTECT, null=False)
    RAM_ID = models.ForeignKey('ModuloMantenedores.Rama', on_delete=models.PROTECT, null=False)


class Persona_Curso(models.Model):
    PEC_ID = models.BigAutoField(primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    CUS_ID = models.ForeignKey('ModuloCursos.Curso_Seccion', on_delete=models.PROTECT, null=False)
    ROL_ID = models.ForeignKey('ModuloMantenedores.Rol', on_delete=models.PROTECT, null=False)
    ALI_ID = models.ForeignKey('ModuloMantenedores.Alimentacion', on_delete=models.PROTECT, blank=True, null=True)
    NIV_ID = models.ForeignKey('ModuloMantenedores.Nivel', on_delete=models.PROTECT, null=True)
    PEC_OBSERVACION = models.CharField(blank=True, null=True)
    PEC_REGISTRO = models.BooleanField(default=False)
    PEC_ACREDITACION = models.BooleanField(default=False)

class Persona_Estado_Curso(models.Model):
    PEU_ID = models.BigAutoField(primary_key=True)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=False)
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False)
    PEU_FECHA_HORA = models.DateTimeField(auto_now_add=True, null=False)
    PEU_ESTADO_OPTIONS = [
        (1, 'Pre Inscrito'),
        (2, 'Avisado'),
        (3, 'Lista de Espera'),
        (4, 'Inscrito'),
        (5, 'Vigente'),
        (6, 'Anulado'),
        (7, 'Sobrecupo'),
    ]
    PEU_ESTADO = models.IntegerField(choices=PEU_ESTADO_OPTIONS, null=False)
    PEU_VIGENTE = models.BooleanField(default=True, null=False)

class Persona_Vehiculo(models.Model): 
    PEV_ID = models.BigAutoField(primary_key=True)
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.PROTECT, null=False) 
    PEV_MARCA = models.CharField(max_length=50, null=False) 
    PEV_MODELO = models.CharField(max_length=50, null=False) 
    PEV_PATENTE = models.CharField(max_length=10, null=False)

class Perfil_Aplicacion(models.Model):
    PEA_ID = models.BigAutoField(primary_key=True)
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False)
    APL_ID = models.ForeignKey('Aplicacion',on_delete=models.PROTECT, null=False)
    PEA_INGRESAR = models.BooleanField(default=False, null=False)
    PEA_MODIFICAR = models.BooleanField(default=False, null=False)
    PEA_ELIMINAR = models.BooleanField(default=False, null=False)
    PEA_CONSULTAR = models.BooleanField(default=False, null=False)