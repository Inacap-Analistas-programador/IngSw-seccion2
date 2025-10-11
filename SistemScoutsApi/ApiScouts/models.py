from django.db import models

# --- Mantenedores Maestros --- #

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

class Perfil_Aplicacion(models.Model):
    PEA_ID = models.BigAutoField(primary_key=True)
    PEL_ID = models.ForeignKey('Perfil',on_delete=models.PROTECT, null=False)
    APL_ID = models.ForeignKey('Aplicacion',on_delete=models.PROTECT, null=False)
    PEA_INGRESAR = models.BooleanField(default=False, null=False)
    PEA_MODIFICAR = models.BooleanField(default=False, null=False)
    PEA_ELIMINAR = models.BooleanField(default=False, null=False)
    PEA_CONSULTAR = models.BooleanField(default=False, null=False)

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

# --- Mantenedores Auxiliares --- #

class Tipo_Archivo(models.Model):
    TAR_ID = models.BigAutoField(primary_key=True)
    TAR_DESCRIPCION = models.CharField(max_length=50, null=False)
    TAR_VIGENTE = models.BooleanField(default=True, null=False)

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
    TCU_TIPO = models.CharField(choices=TCU_TIPO_OPCION, null=False)
    TCU_CANT_PARTICIPANTE = models.IntegerField(null=False)
    TCU_VIGENTE = models.BooleanField(default=True, null=False)

class Alimentacion(models.Model):
    ALI_ID = models.BigAutoField(primary_key=True)
    ALI_DESCRIPCION = models.CharField(max_length=100, null=False)
    ALI_TIPO_OPCION = [
        (1, 'Con Almuerzo'),
        (2, 'Sin Almuerzo'),
    ]
    ALI_TIPO = models.IntegerField(choices=ALI_TIPO_OPCION, null=False)
    ALI_VIGENTE = models.BooleanField(default=True, null=False)

class Rol(models.Model):
    ROL_ID = models.BigAutoField(primary_key=True)
    ROL_DESCRIPCION = models.CharField(max_length=50, null=False)
    ROL_TIPO = models.IntegerField(null=False)
    ROL_VIGENTE = models.BooleanField(default=True, null=False)

class Cargo(models.Model):
    CAR_ID = models.BigAutoField(primary_key=True)
    CAR_DESCRIPCION = models.CharField(max_length=100, null=False)
    CAR_VIGENTE = models.BooleanField(default=True, null=False)

class Concepto_Contable(models.Model):
    COC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    COC_DESCRIPCION = models.CharField(max_length=100)
    COC_VIGENTE = models.BooleanField(default=True)

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

    # --- Gestion de Usuario --- #

class Persona(models.Model):
    PER_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ESC_ID = models.ForeignKey('Estado_Civil', on_delete=models.CASCADE)
    COM_ID = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    PER_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    PER_RUN = models.CharField(max_length=9, unique=True)
    PER_DV = models.CharField(max_length=1)
    PER_APELPTA = models.CharField(max_length=50)
    PER_APELMAT = models.CharField(max_length=50)
    PER_NOMBRES = models.CharField(max_length=50)
    PER_MAIL = models.CharField(max_length=100)
    PER_FECHA_NAC = models.DateField()
    PER_DIRECCION = models.CharField(max_length=255)
    PER_TIPO_FONO = models.Choices('1', 'Fijo'), ('2', 'Celular')
    PER_FONO = models.CharField(max_length=15, blank=True, null=True)
    PER_ALERGIA_ENFERMEDAD = models.CharField(max_length=255, blank=True, null=True)
    PER_LIMITACION = models.CharField(max_length=255, blank=True, null=True)
    PER_NOM_EMERGENCIA = models.CharField(max_length=50, blank=True, null=True)
    PER_FONO_EMERGENCIA = models.CharField(max_length=15, blank=True, null=True)
    PER_OTROS = models.CharField(max_length=255, blank=True, null=True)
    PER_NUM_MMA = models.IntegerField(blank=True, null=True)
    PER_PROFESION = models.CharField(max_length=100, blank=True, null=True)
    PER_TIEMPO_NNAJ = models.CharField(max_length=100, blank=True, null=True)
    PER_TIEMPO_ADULTO = models.CharField(max_length=100, blank=True, null=True)
    PER_RELIGION = models.CharField(max_length=100, blank=True, null=True)
    PER_APODO = models.CharField(max_length=50, blank=True, null=True)
    PER_FOTO = models.CharField(max_length=255, blank=True, null=True)
    PER_VIGENTE = models.BooleanField(default=True)

class Persona_Grupo(models.Model):
    PEG_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    GRU_ID = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    PEG_VIGENTE = models.BooleanField(default=True)

class Persona_Formador(models.Model):
    PEF_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    PEF_HAB_1 = models.BooleanField(default=False)
    PEF_HAB_2 = models.BooleanField(default=False)
    PEF_VERIF = models.BooleanField(default=False)
    PEF_HISTORIAL = models.CharField(blank=True, null=True)

class Persona_Individual(models.Model):
    PEI_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CAR_ID = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    DIS_ID = models.ForeignKey('Distrito', on_delete=models.CASCADE)
    ZON_ID = models.ForeignKey('Zona', on_delete=models.CASCADE)
    PEI_VIGENTE = models.BooleanField(default=True)

class Persona_Nivel(models.Model):
    PEN_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    NIV_ID = models.ForeignKey('Nivel', on_delete=models.CASCADE)
    RAM_ID = models.ForeignKey('Rama', on_delete=models.CASCADE)

# --- Gestion Cursos --- #

class Curso(models.Model):
    CURS_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE)
    PER_ID_RESPONSABLE = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CAR_ID_RESPONSABLE = models.ForeignKey('Cargo', on_delete=models.CASCADE, related_name='cargo_responsable')
    COM_ID_LUGAR = models.ForeignKey('Comuna', on_delete=models.CASCADE, related_name='comuna_lugar')
    CUR_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    CUR_FECHA_SOLICITUD = models.DateField()
    CUR_CODIGO = models.CharField(max_length=20, unique=True)
    CUR_DESCRIPCION = models.CharField(max_length=255)
    CUR_OBSERVACION = models.CharField(max_length=255, blank=True, null=True)
    #CUR_ADMINISTRA = 
    CUR_COTA_CON_ALMUERZO = models.IntegerField()
    CUR_COTA_SIN_ALMUERZO = models.IntegerField()
    CUR_MODALIDAD = models.IntegerField()
    #CUR_TIPO_CURSO =
    CUR_LUGAR = models.CharField(max_length=100)
    #CUR_ESTADO = 

class Curso_Cuota(models.Model):
    CUU_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    CUU_TIPO = models.IntegerField()
    CUU_FECHA = models.DateField()
    CUU_VALOR = models.IntegerField()

class Curso_Fecha(models.Model):
    CUF_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    CUF_FECHA_INICIO = models.DateField()
    CUF_FECHA_TERMINO = models.DateField()
    CUF_TIPO = models.IntegerField()

class Curso_Alimentacion(models.Model):
    CUA_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    ALI_ID = models.ForeignKey('Alimentacion', on_delete=models.CASCADE)
    CUA_FECHA = models.DateField()
    CUA_TIEMPO = models.IntegerField()
    CUA_DESCRIPCION = models.CharField(max_length=100)
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0)
    CUA_VIGENTE = models.BooleanField(default=True)

class Curso_Coordinador(models.Model):
    CUC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CAR_ID = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    CUC_CARGO = models.CharField(max_length=100)

class Curso_Seccion(models.Model):
    CUS_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    RAM_ID = models.ForeignKey('Rama', on_delete=models.CASCADE)
    CUS_SECCION = models.IntegerField()
    CUS_CANT_PARTICIPANTE = models.IntegerField()

class Curso_Formador(models.Model):
    CUF_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    ROL_ID = models.ForeignKey('Rol', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.CASCADE, blank=True, null=True)
    CUO_DIRECTOR = models.IntegerField()

# --- Gestion de Usuario --- #

class Persona_Curso(models.Model):
    PEC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.CASCADE)
    ROL_ID = models.ForeignKey('Rol', on_delete=models.CASCADE)
    ALI_ID = models.ForeignKey('Alimentacion', on_delete=models.CASCADE, blank=True, null=True)
    NIV_ID = models.ForeignKey('Nivel', on_delete=models.CASCADE)
    PEC_OBSERVACION = models.CharField(blank=True, null=True)
    PEC_REGISTRO = models.BooleanField(default=False)
    PEC_ACREDITACION = models.BooleanField(default=False)

# --- Gestion de Archivos --- #

class Archivo(models.Model):
    ARC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    TAR_ID = models.ForeignKey('Tipo_Archivo', on_delete=models.CASCADE)
    USU_ID_CREA = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='usuario_crea')
    USU_ID_MODIFICA = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='usuario_modifica', blank=True, null=True)
    ARC_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    ARC_DESCRIPCION = models.CharField(max_length=100)
    ARC_RUTA = models.CharField()
    ARC_VIGENTE = models.BooleanField(default=True)

class Archivo_Curso(models.Model):
    ARU_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)

class Archivo_Persona(models.Model):
    ARP_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    ARC_ID = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('Persona', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('Curso', on_delete=models.CASCADE, blank=True, null=True)

# --- Estados y Transporte por Curso --- #

class Persona_Vehiculo(models.Model):
    PEV_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.CASCADE)
    PEV_MARCA = models.CharField(max_length=50)
    PEV_MODELO = models.CharField(max_length=50)
    PEV_PATENTE = models.CharField(max_length=10)

class Persona_Estado_Curso(models.Model):
    PEU_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    USU_ID = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    PEC_ID = models.ForeignKey('Persona_Curso', on_delete=models.CASCADE)
    PEU_FECHA_HORA = models.DateTimeField(auto_now_add=True)
    PEU_ESTADO = models.IntegerField()
    PEU_VIGENTE = models.BooleanField(default=True)

# --- Gestion de Pagos --- #



# --- Proveedores --- #

class Proveedor(models.Model):
    PRV_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    PRV_DESCRIPCION = models.CharField(max_length=100)
    PRV_CELULAR1 = models.CharField(max_length=15, blank=True, null=True)
    PRV_CELULAR2 = models.CharField(max_length=15, blank=True, null=True)
    PRV_DIRECCION = models.CharField(max_length=100, blank=True, null=True)
    PRV_OBSERVACION = models.CharField(blank=True, null=True)
    PRV_VIGENTE = models.BooleanField(default=True)
