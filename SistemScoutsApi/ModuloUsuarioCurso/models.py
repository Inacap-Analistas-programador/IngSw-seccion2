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
    PEF_HISTORIAL = models.CharField(max_length=500, blank=True, null=True)

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
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False)
    ROL_ID = models.ForeignKey('ModuloMantenedores.Rol', on_delete=models.PROTECT, null=False)
    ALI_ID = models.ForeignKey('ModuloMantenedores.Alimentacion', on_delete=models.PROTECT, blank=True, null=True)
    NIV_ID = models.ForeignKey('ModuloMantenedores.Nivel', on_delete=models.PROTECT, null=True)
    PEC_OBSERVACION = models.CharField(max_length=500, blank=True, null=True)
    PEC_REGISTRO = models.BooleanField(default=False, null=False)
    PEC_ACREDITACION = models.BooleanField(default=False, null=False)

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

class Curso(models.Model):
    CURS_ID = models.BigAutoField(primary_key=True)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE)
    PER_ID_RESPONSABLE = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CAR_ID_RESPONSABLE = models.ForeignKey('ModuloMantenedores.Cargo', on_delete=models.CASCADE, related_name='cargo_responsable')
    COM_ID_LUGAR = models.ForeignKey('ModuloMantenedores.Comuna', on_delete=models.CASCADE, related_name='comuna_lugar')
    CUR_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    CUR_FECHA_SOLICITUD = models.DateField()
    CUR_CODIGO = models.CharField(max_length=20, unique=True)
    CUR_DESCRIPCION = models.CharField(max_length=255)
    CUR_OBSERVACION = models.CharField(max_length=255, blank=True, null=True)
    CUR_ADMINISTRA_OPCION = [
        (2, 'Zona'),
        (2, 'Distrito'),
    ]
    CUR_ADMINISTRA = models.IntegerField(choices=CUR_ADMINISTRA_OPCION, null=False)
    CUR_COTA_CON_ALMUERZO = models.IntegerField()
    CUR_COTA_SIN_ALMUERZO = models.IntegerField()
    CUR_MODALIDAD_OPTIONS = [
        (1, 'Internado'),
        (2, 'Externado'),
        (3, 'Internado/Externado'),
    ]
    CUR_MODALIDAD = models.IntegerField(choices=CUR_MODALIDAD_OPTIONS, null=False)
    CUR_TIPO_CURSO_OPTIONS = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUR_TIPO_CURSO = models.IntegerField(choices=CUR_TIPO_CURSO_OPTIONS, null=False)
    CUR_LUGAR = models.CharField(max_length=100)
    CUR_ESTADO_OPTIONS = [
        (0, 'Pendiente'),
        (1, 'Vigente'),
        (2, 'Anulado'),
        (3, 'Finalizado'),
    ]
    CUR_ESTADO = models.IntegerField(choices=CUR_ESTADO_OPTIONS, null=False)

class Curso_Cuota(models.Model):
    CUU_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    CUU_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    CUU_TIPO = models.IntegerField(choices=CUU_TIPO_OPCION, null=False)
    CUU_FECHA = models.DateField(null=False)
    CUU_VALOR = models.DecimalField(max_digits=21,decimal_places=6, null=False)

class Curso_Fecha(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    CUF_FECHA_INICIO = models.DateField(null=False)
    CUF_FECHA_TERMINO = models.DateField(null=False)
    CUF_TIPO_OPCION = [
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'Hibrido'),
    ]
    CUF_TIPO = models.IntegerField(choices=CUF_TIPO_OPCION, null=False)

class Curso_Alimentacion(models.Model):
    CUA_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    ALI_ID = models.ForeignKey('ModuloMantenedores.Alimentacion', on_delete=models.PROTECT, null=False)
    CUA_FECHA = models.DateField()
    CUA_TIEMPO_OPCION = [
        (1, 'Desayuno'),
        (2, 'Almuerzo'),
        (3, 'Once'),
        (4, 'Cena'),
        (5, 'Once/Cena'),
    ]
    CUA_TIEMPO = models.IntegerField(choices=CUA_TIEMPO_OPCION, null=False)
    CUA_DESCRIPCION = models.CharField(max_length=100, null=False)
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0, null=False)
    CUA_VIGENTE = models.BooleanField(default=True, null=False)

class Curso_Coordinador(models.Model):
    CUC_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    CAR_ID = models.ForeignKey('ModuloMantenedores.Cargo', on_delete=models.PROTECT, null=False)
    CUC_CARGO = models.CharField(max_length=100, null=True)

class Curso_Seccion(models.Model):
    CUS_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    RAM_ID = models.ForeignKey('ModuloMantenedores.Rama', on_delete=models.PROTECT, null=True)
    CUS_SECCION = models.IntegerField(null=False)
    CUS_CANT_PARTICIPANTE = models.IntegerField(null=False)

class Curso_Formador(models.Model):
    CUF_ID = models.BigAutoField(primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.PROTECT, null=False)
    PER_ID = models.ForeignKey('Persona', on_delete=models.PROTECT, null=False)
    ROL_ID = models.ForeignKey('ModuloMantenedores.Rol', on_delete=models.PROTECT, null=False)
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.PROTECT, null=False)
    CUO_DIRECTOR = models.BooleanField(default=False, null=False)

class Tipo_Curso(models.Model):
    TCU_ID = models.BigAutoField(primary_key=True)
    TCU_DESCRIPCION = models.CharField(max_length=100, null=False)
    TCU_TIPO_OPCION = [
        (1, 'Inicial'),
        (2, 'Medio'),
        (3, 'Avanzado'),
        (4, 'Habilitación'),
        (5, 'Verificación'),
        (6, 'Institucional'),
    ]
    TCU_TIPO = models.IntegerField(choices=TCU_TIPO_OPCION, null=False)
    TCU_CANT_PARTICIPANTE = models.IntegerField(null=True)
    TCU_VIGENTE = models.BooleanField(default=True, null=False)
