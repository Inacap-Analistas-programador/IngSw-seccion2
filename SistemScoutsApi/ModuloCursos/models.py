from django.db import models

class Curso(models.Model):
    CURS_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    USU_ID = models.ForeignKey('ModuloUsuarios.Usuario', on_delete=models.CASCADE)
    TCU_ID = models.ForeignKey('Tipo_Curso', on_delete=models.CASCADE)
    PER_ID_RESPONSABLE = models.ForeignKey('ModuloUsuarios.Persona', on_delete=models.CASCADE)
    CAR_ID_RESPONSABLE = models.ForeignKey('ModuloMantenedores.Cargo', on_delete=models.CASCADE, related_name='cargo_responsable')
    COM_ID_LUGAR = models.ForeignKey('ModuloMantenedores.Comuna', on_delete=models.CASCADE, related_name='comuna_lugar')
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
    ALI_ID = models.ForeignKey('ModuloMantenedores.Alimentacion', on_delete=models.CASCADE)
    CUA_FECHA = models.DateField()
    CUA_TIEMPO = models.IntegerField()
    CUA_DESCRIPCION = models.CharField(max_length=100)
    CUA_CANTIDAD_ADICIONAL = models.IntegerField(default=0)
    CUA_VIGENTE = models.BooleanField(default=True)

class Curso_Coordinador(models.Model):
    CUC_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('ModuloUsuarios.Persona', on_delete=models.CASCADE)
    CAR_ID = models.ForeignKey('ModuloMantenedores.Cargo', on_delete=models.CASCADE)
    CUC_CARGO = models.CharField(max_length=100)

class Curso_Seccion(models.Model):
    CUS_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    RAM_ID = models.ForeignKey('ModuloMantenedores.Rama', on_delete=models.CASCADE)
    CUS_SECCION = models.IntegerField()
    CUS_CANT_PARTICIPANTE = models.IntegerField()

class Curso_Formador(models.Model):
    CUF_ID = models.CharField(max_length=10, unique=True, primary_key=True)
    CUR_ID = models.ForeignKey('Curso', on_delete=models.CASCADE)
    PER_ID = models.ForeignKey('ModuloUsuarios.Persona', on_delete=models.CASCADE)
    ROL_ID = models.ForeignKey('ModuloMantenedores.Rol', on_delete=models.CASCADE)
    CUS_ID = models.ForeignKey('Curso_Seccion', on_delete=models.CASCADE, blank=True, null=True)
    CUO_DIRECTOR = models.IntegerField()

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
