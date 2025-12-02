from rest_framework import serializers
from ..Models.persona_model import *

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class PersonaCompletaSerializer(serializers.ModelSerializer):
    """Serializer que incluye datos relacionados de rol, rama y grupo"""
    per_rol = serializers.SerializerMethodField()
    per_rama = serializers.SerializerMethodField()
    per_grupo = serializers.SerializerMethodField()
    
    # Campos de Grupo Scout
    gru_id = serializers.SerializerMethodField()
    peg_vigente = serializers.SerializerMethodField()
    
    # Campos de Formador
    pef_hab_1 = serializers.SerializerMethodField()
    pef_hab_2 = serializers.SerializerMethodField()
    pef_verif = serializers.SerializerMethodField()
    pef_historial = serializers.SerializerMethodField()
    
    # Campos de Individual
    car_id = serializers.SerializerMethodField()
    dis_id = serializers.SerializerMethodField()
    zon_id = serializers.SerializerMethodField()
    pei_vigente = serializers.SerializerMethodField()
    
    # Campos de Nivel
    niv_id = serializers.SerializerMethodField()
    ram_id_nivel = serializers.SerializerMethodField()
    
    # Campos de Vehículo
    pev_patente = serializers.SerializerMethodField()
    pev_marca = serializers.SerializerMethodField()
    pev_modelo = serializers.SerializerMethodField()
    pev_anio = serializers.SerializerMethodField()
    pev_color = serializers.SerializerMethodField()
    pev_capacidad = serializers.SerializerMethodField()
    
    class Meta:
        model = Persona
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convertir Decimal a int para campos ID
        if 'per_id' in ret and ret['per_id'] is not None:
            ret['per_id'] = int(ret['per_id'])
        if 'usu_id' in ret and ret['usu_id'] is not None:
            ret['usu_id'] = int(ret['usu_id'])
        if 'esc_id' in ret and ret['esc_id'] is not None:
            ret['esc_id'] = int(ret['esc_id'])
        if 'com_id' in ret and ret['com_id'] is not None:
            ret['com_id'] = int(ret['com_id'])
        # Convertir otros campos enteros que podrían ser Decimal
        if 'per_num_mma' in ret and ret['per_num_mma'] is not None:
            ret['per_num_mma'] = int(ret['per_num_mma'])
        if 'per_tipo_fono' in ret and ret['per_tipo_fono'] is not None:
            ret['per_tipo_fono'] = int(ret['per_tipo_fono'])
        # Convertir RUN y DV si vienen como Decimal
        if 'per_run' in ret and ret['per_run'] is not None:
            ret['per_run'] = str(int(ret['per_run']))
        if 'per_dv' in ret and ret['per_dv'] is not None:
            ret['per_dv'] = str(ret['per_dv'])
        return ret

    def get_per_rol(self, obj):
        """Obtener rol desde persona_curso (último rol activo)"""
        try:
            persona_curso = Persona_Curso.objects.filter(per_id=obj.per_id).first()
            if persona_curso and persona_curso.rol_id:
                return persona_curso.rol_id.rol_descripcion
        except:
            pass
        return None
    
    def get_per_rama(self, obj):
        """Obtener rama desde persona_nivel"""
        try:
            persona_nivel = Persona_Nivel.objects.filter(per_id=obj.per_id).first()
            if persona_nivel and persona_nivel.ram_id:
                return persona_nivel.ram_id.ram_descripcion
        except:
            pass
        return None
    
    def get_per_grupo(self, obj):
        """Obtener grupo desde persona_grupo"""
        try:
            persona_grupo = Persona_Grupo.objects.filter(per_id=obj.per_id).first()
            if persona_grupo and persona_grupo.gru_id:
                return persona_grupo.gru_id.gru_descripcion
        except:
            pass
        return None
    
    # Métodos para Grupo Scout
    def get_gru_id(self, obj):
        try:
            persona_grupo = Persona_Grupo.objects.filter(per_id=obj.per_id).first()
            if persona_grupo and persona_grupo.gru_id:
                return int(persona_grupo.gru_id.gru_id)
        except:
            pass
        return None
    
    def get_peg_vigente(self, obj):
        try:
            persona_grupo = Persona_Grupo.objects.filter(per_id=obj.per_id).first()
            if persona_grupo:
                return persona_grupo.peg_vigente
        except:
            pass
        return None
    
    # Métodos para Formador
    def get_pef_hab_1(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(per_id=obj.per_id).first()
            if persona_formador:
                return persona_formador.pef_hab_1
        except:
            pass
        return None
    
    def get_pef_hab_2(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(per_id=obj.per_id).first()
            if persona_formador:
                return persona_formador.pef_hab_2
        except:
            pass
        return None
    
    def get_pef_verif(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(per_id=obj.per_id).first()
            if persona_formador:
                return persona_formador.pef_verif
        except:
            pass
        return None
    
    def get_pef_historial(self, obj):
        try:
            persona_formador = Persona_Formador.objects.filter(per_id=obj.per_id).first()
            if persona_formador:
                return persona_formador.pef_historial
        except:
            pass
        return None
    
    # Métodos para Individual
    def get_car_id(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(per_id=obj.per_id).first()
            if persona_individual and persona_individual.car_id:
                return int(persona_individual.car_id.car_id)
        except:
            pass
        return None
    
    def get_dis_id(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(per_id=obj.per_id).first()
            if persona_individual and persona_individual.dis_id:
                return int(persona_individual.dis_id.dis_id)
        except:
            pass
        return None
    
    def get_zon_id(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(per_id=obj.per_id).first()
            if persona_individual and persona_individual.zon_id:
                return int(persona_individual.zon_id.zon_id)
        except:
            pass
        return None
    
    def get_pei_vigente(self, obj):
        try:
            persona_individual = Persona_Individual.objects.filter(per_id=obj.per_id).first()
            if persona_individual:
                return persona_individual.pei_vigente
        except:
            pass
        return None
    
    # Métodos para Nivel
    def get_niv_id(self, obj):
        try:
            persona_nivel = Persona_Nivel.objects.filter(per_id=obj.per_id).first()
            if persona_nivel and persona_nivel.niv_id:
                return int(persona_nivel.niv_id.niv_id)
        except:
            pass
        return None
    
    def get_ram_id_nivel(self, obj):
        try:
            persona_nivel = Persona_Nivel.objects.filter(per_id=obj.per_id).first()
            if persona_nivel and persona_nivel.ram_id:
                return int(persona_nivel.ram_id.ram_id)
        except:
            pass
        return None
    
    # Métodos para Vehículo
    def get_pev_patente(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_patente
        except:
            pass
        return None
    
    def get_pev_marca(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_marca
        except:
            pass
        return None
    
    def get_pev_modelo(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_modelo
        except:
            pass
        return None
    
    def get_pev_anio(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_anio
        except:
            pass
        return None
    
    def get_pev_color(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_color
        except:
            pass
        return None
    
    def get_pev_capacidad(self, obj):
        try:
            persona_vehiculo = Persona_Vehiculo.objects.filter(per_id=obj.per_id).first()
            if persona_vehiculo:
                return persona_vehiculo.pev_capacidad
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
    cur_nombre = serializers.SerializerMethodField()
    cur_descripcion = serializers.SerializerMethodField()
    cur_fechainicio = serializers.SerializerMethodField()
    cur_fechafin = serializers.SerializerMethodField()
    cur_codigo = serializers.SerializerMethodField()
    rol_descripcion = serializers.SerializerMethodField()
    estado_aprobacion = serializers.SerializerMethodField()
    
    class Meta:
        model = Persona_Curso
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convertir Decimal a int para campos ID
        if 'pec_id' in ret and ret['pec_id'] is not None:
            ret['pec_id'] = int(ret['pec_id'])
        if 'per_id' in ret and ret['per_id'] is not None:
            ret['per_id'] = int(ret['per_id'])
        if 'cus_id' in ret and ret['cus_id'] is not None:
            ret['cus_id'] = int(ret['cus_id'])
        if 'rol_id' in ret and ret['rol_id'] is not None:
            ret['rol_id'] = int(ret['rol_id'])
        if 'ali_id' in ret and ret['ali_id'] is not None:
            ret['ali_id'] = int(ret['ali_id'])
        if 'niv_id' in ret and ret['niv_id'] is not None:
            ret['niv_id'] = int(ret['niv_id'])
        # Convertir booleanos que pueden venir como números
        if 'pec_registro' in ret and ret['pec_registro'] is not None:
            ret['pec_registro'] = bool(ret['pec_registro'])
        if 'pec_acreditacion' in ret and ret['pec_acreditacion'] is not None:
            ret['pec_acreditacion'] = bool(ret['pec_acreditacion'])
        if 'pec_envio_correo_qr' in ret and ret['pec_envio_correo_qr'] is not None:
            ret['pec_envio_correo_qr'] = bool(ret['pec_envio_correo_qr'])
        return ret
    
    def get_cur_nombre(self, obj):
        try:
            if obj.cus_id and obj.cus_id.cur_id:
                return obj.cus_id.cur_id.cur_descripcion
        except:
            pass
        return None
    
    def get_cur_descripcion(self, obj):
        try:
            if obj.cus_id and obj.cus_id.cur_id:
                return obj.cus_id.cur_id.cur_descripcion
        except:
            pass
        return None
    
    def get_cur_fechainicio(self, obj):
        try:
            if obj.cus_id and obj.cus_id.cur_id:
                # Intentar obtener fecha de solicitud como fallback
                return obj.cus_id.cur_id.cur_fecha_solicitud
        except:
            pass
        return None
    
    def get_cur_fechafin(self, obj):
        try:
            # No hay campo directo en Curso, retornar None por ahora
            pass
        except:
            pass
        return None
    
    def get_cur_codigo(self, obj):
        try:
            if obj.cus_id and obj.cus_id.cur_id:
                return obj.cus_id.cur_id.cur_codigo
        except:
            pass
        return None
    
    def get_rol_descripcion(self, obj):
        try:
            if obj.rol_id:
                return obj.rol_id.rol_descripcion
        except:
            pass
        return None
    
    def get_estado_aprobacion(self, obj):
        """Retorna el estado de aprobación del curso"""
        return {
            'aprobado': bool(obj.pec_acreditacion),
            'texto': 'Aprobado' if obj.pec_acreditacion else 'No Aprobado'
        }

class PersonaEstadoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Estado_Curso
        fields = '__all__'

class PersonaVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona_Vehiculo
        fields = '__all__'
