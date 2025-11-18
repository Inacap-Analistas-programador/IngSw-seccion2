from rest_framework import serializers
from ..Models.persona_model import *

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class PersonaCompletaSerializer(serializers.ModelSerializer):
    """Serializer que incluye datos relacionados de rol, rama y grupo"""
    PER_ROL = serializers.SerializerMethodField()
    PER_RAMA = serializers.SerializerMethodField()
    PER_GRUPO = serializers.SerializerMethodField()
    
    # Campos de Grupo Scout
    GRU_ID = serializers.SerializerMethodField()
    PEG_VIGENTE = serializers.SerializerMethodField()
    
    # Campos de Formador
    PEF_HAB_1 = serializers.SerializerMethodField()
    PEF_HAB_2 = serializers.SerializerMethodField()
    PEF_VERIF = serializers.SerializerMethodField()
    PEF_HISTORIAL = serializers.SerializerMethodField()
    
    # Campos de Individual
    CAR_ID = serializers.SerializerMethodField()
    DIS_ID = serializers.SerializerMethodField()
    ZON_ID = serializers.SerializerMethodField()
    PEI_VIGENTE = serializers.SerializerMethodField()
    
    # Campos de Nivel
    NIV_ID = serializers.SerializerMethodField()
    RAM_ID_NIVEL = serializers.SerializerMethodField()
    
    # Campos de Vehículo
    PEV_PATENTE = serializers.SerializerMethodField()
    PEV_MARCA = serializers.SerializerMethodField()
    PEV_MODELO = serializers.SerializerMethodField()
    PEV_ANIO = serializers.SerializerMethodField()
    PEV_COLOR = serializers.SerializerMethodField()
    PEV_CAPACIDAD = serializers.SerializerMethodField()
    
    class Meta:
        model = Persona
        fields = '__all__'
    
    def get_PER_ROL(self, obj):
        """Obtener rol desde persona_curso (último rol activo)"""
        try:
            persona_curso = Persona_Curso.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_curso and persona_curso.ROL_ID:
                return persona_curso.ROL_ID.ROL_DESCRIPCION
        except:
            pass
        return None
    
    def get_PER_RAMA(self, obj):
        """Obtener rama desde persona_nivel"""
        try:
            persona_nivel = Persona_Nivel.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_nivel and persona_nivel.RAM_ID:
                return persona_nivel.RAM_ID.RAM_DESCRIPCION
        except:
            pass
        return None
    
    def get_PER_GRUPO(self, obj):
        """Obtener grupo desde persona_grupo"""
        try:
            persona_grupo = Persona_Grupo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_grupo and persona_grupo.GRU_ID:
                return persona_grupo.GRU_ID.GRU_DESCRIPCION
        except:
            pass
        return None
    
    # Métodos para Grupo Scout
    def get_GRU_ID(self, obj):
        try:
            persona_grupo = Persona_Grupo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_grupo and persona_grupo.GRU_ID:
                return persona_grupo.GRU_ID.GRU_ID
        except:
            pass
        return None
    
    def get_PEG_VIGENTE(self, obj):
        try:
            persona_grupo = Persona_Grupo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_grupo:
                return persona_grupo.PEG_VIGENTE
        except:
            pass
        return None
    
    # Métodos para Formador
    def get_PEF_HAB_1(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_formador:
                return persona_formador.PEF_HAB_1
        except:
            pass
        return None
    
    def get_PEF_HAB_2(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_formador:
                return persona_formador.PEF_HAB_2
        except:
            pass
        return None
    
    def get_PEF_VERIF(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_formador:
                return persona_formador.PEF_VERIF
        except:
            pass
        return None
    
    def get_PEF_HISTORIAL(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_formador:
                return persona_formador.PEF_HISTORIAL
        except:
            pass
        return None
    
    # Métodos para Individual
    def get_CAR_ID(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_individual and persona_individual.CAR_ID:
                return persona_individual.CAR_ID.CAR_ID
        except:
            pass
        return None
    
    def get_DIS_ID(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_individual and persona_individual.DIS_ID:
                return persona_individual.DIS_ID.DIS_ID
        except:
            pass
        return None
    
    def get_ZON_ID(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_individual and persona_individual.ZON_ID:
                return persona_individual.ZON_ID.ZON_ID
        except:
            pass
        return None
    
    def get_PEI_VIGENTE(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_individual:
                return persona_individual.PEI_VIGENTE
        except:
            pass
        return None
    
    # Métodos para Nivel
    def get_NIV_ID(self, obj):
        try:
            persona_nivel = Persona_Nivel.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_nivel and persona_nivel.NIV_ID:
                return persona_nivel.NIV_ID.NIV_ID
        except:
            pass
        return None
    
    def get_RAM_ID_NIVEL(self, obj):
        try:
            persona_nivel = Persona_Nivel.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_nivel and persona_nivel.RAM_ID:
                return persona_nivel.RAM_ID.RAM_ID
        except:
            pass
        return None
    
    # Métodos para Vehículo
    def get_PEV_PATENTE(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_PATENTE
        except:
            pass
        return None
    
    def get_PEV_MARCA(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_MARCA
        except:
            pass
        return None
    
    def get_PEV_MODELO(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_MODELO
        except:
            pass
        return None
    
    def get_PEV_ANIO(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_ANIO
        except:
            pass
        return None
    
    def get_PEV_COLOR(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_COLOR
        except:
            pass
        return None
    
    def get_PEV_CAPACIDAD(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(PER_ID=obj.PER_ID).first()
            if persona_vehiculo:
                return persona_vehiculo.PEV_CAPACIDAD
        except:
            pass
        return None

class PersonaGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Grupo
        fields = '__all__'

class PersonaFormadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Formador
        fields = '__all__'

class PersonaIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Individual
        fields = '__all__'

class PersonaNivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Nivel
        fields = '__all__'

class PersonaCursoSerializer(serializers.ModelSerializer):
    # Incluir información completa del curso
    CUR_NOMBRE = serializers.SerializerMethodField()
    CUR_DESCRIPCION = serializers.SerializerMethodField()
    CUR_FECHAINICIO = serializers.SerializerMethodField()
    CUR_FECHAFIN = serializers.SerializerMethodField()
    CUR_CODIGO = serializers.SerializerMethodField()
    ROL_DESCRIPCION = serializers.SerializerMethodField()
    ESTADO_APROBACION = serializers.SerializerMethodField()
    
    class Meta:
        model = Persona_Curso
        fields = '__all__'
    
    def get_CUR_NOMBRE(self, obj):
        try:
            if obj.CUS_ID:
                return obj.CUS_ID.CUR_NOMBRE
        except:
            pass
        return None
    
    def get_CUR_DESCRIPCION(self, obj):
        try:
            if obj.CUS_ID:
                return obj.CUS_ID.CUR_DESCRIPCION
        except:
            pass
        return None
    
    def get_CUR_FECHAINICIO(self, obj):
        try:
            if obj.CUS_ID:
                return obj.CUS_ID.CUR_FECHAINICIO
        except:
            pass
        return None
    
    def get_CUR_FECHAFIN(self, obj):
        try:
            if obj.CUS_ID:
                return obj.CUS_ID.CUR_FECHAFIN
        except:
            pass
        return None
    
    def get_CUR_CODIGO(self, obj):
        try:
            if obj.CUS_ID:
                return obj.CUS_ID.CUR_CODIGO
        except:
            pass
        return None
    
    def get_ROL_DESCRIPCION(self, obj):
        try:
            if obj.ROL_ID:
                return obj.ROL_ID.ROL_DESCRIPCION
        except:
            pass
        return None
    
    def get_ESTADO_APROBACION(self, obj):
        """Retorna el estado de aprobación del curso"""
        return {
            'aprobado': bool(obj.PEC_ACREDITACION),
            'texto': 'Aprobado' if obj.PEC_ACREDITACION else 'No Aprobado'
        }

class PersonaEstadoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Estado_Curso
        fields = '__all__'

class PersonaVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Vehiculo
        fields = '__all__'
