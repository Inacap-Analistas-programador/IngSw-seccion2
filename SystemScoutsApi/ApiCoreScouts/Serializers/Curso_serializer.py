from rest_framework import serializers
from ..Models.curso_model import *

class CursoCuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Cuota
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'cuu_id' in ret and ret['cuu_id'] is not None:
            ret['cuu_id'] = int(ret['cuu_id'])
        if 'cur_id' in ret and ret['cur_id'] is not None:
            ret['cur_id'] = int(ret['cur_id'])
        if 'cuu_tipo' in ret and ret['cuu_tipo'] is not None:
            ret['cuu_tipo'] = int(ret['cuu_tipo'])
        if 'cuu_valor' in ret and ret['cuu_valor'] is not None:
            try:
                ret['cuu_valor'] = int(float(ret['cuu_valor']))
            except (ValueError, TypeError):
                pass
        return ret

class CursoFechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Fecha
        fields = '__all__'

class CursoAlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Alimentacion
        fields = '__all__'

class CursoCoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Coordinador
        fields = '__all__'

class CursoSeccionSerializer(serializers.ModelSerializer):
    sec_descripcion = serializers.SerializerMethodField()

    class Meta:
        model = Curso_Seccion
        fields = '__all__'

    def get_sec_descripcion(self, obj):
        rama_desc = obj.ram_id.ram_descripcion if obj.ram_id else "Sin Rama"
        return f"seccion {obj.cus_seccion} - rama {rama_desc}"

class CursoFormadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso_Formador
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    fechas = CursoFechaSerializer(many=True, read_only=True, source='curso_fecha_set')
    secciones = CursoSeccionSerializer(many=True, read_only=True, source='curso_seccion_set')
    formadores = CursoFormadorSerializer(many=True, read_only=True, source='curso_formador_set')
    alimentacion = CursoAlimentacionSerializer(many=True, read_only=True, source='curso_alimentacion_set')
    cuotas = CursoCuotaSerializer(many=True, read_only=True, source='curso_cuota_set')
    coordinadores = CursoCoordinadorSerializer(many=True, read_only=True, source='curso_coordinador_set')

    class Meta:
        model = Curso
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convertir Decimal a int para campos ID
        if 'cur_id' in ret and ret['cur_id'] is not None:
            ret['cur_id'] = int(ret['cur_id'])
        if 'usu_id' in ret and ret['usu_id'] is not None:
            ret['usu_id'] = int(ret['usu_id'])
        if 'tcu_id' in ret and ret['tcu_id'] is not None:
            ret['tcu_id'] = int(ret['tcu_id'])
        if 'per_id_responsable' in ret and ret['per_id_responsable'] is not None:
            ret['per_id_responsable'] = int(ret['per_id_responsable'])
        if 'car_id_responsable' in ret and ret['car_id_responsable'] is not None:
            ret['car_id_responsable'] = int(ret['car_id_responsable'])
        if 'com_id_lugar' in ret and ret['com_id_lugar'] is not None:
            ret['com_id_lugar'] = int(ret['com_id_lugar'])
        # Convertir otros campos enteros
        if 'cur_administra' in ret and ret['cur_administra'] is not None:
            ret['cur_administra'] = int(ret['cur_administra'])
        if 'cur_cota_con_almuerzo' in ret and ret['cur_cota_con_almuerzo'] is not None:
            try:
                ret['cur_cota_con_almuerzo'] = int(float(ret['cur_cota_con_almuerzo']))
            except (ValueError, TypeError):
                pass
        if 'cur_cota_sin_almuerzo' in ret and ret['cur_cota_sin_almuerzo'] is not None:
            try:
                ret['cur_cota_sin_almuerzo'] = int(float(ret['cur_cota_sin_almuerzo']))
            except (ValueError, TypeError):
                pass
        if 'cur_modalidad' in ret and ret['cur_modalidad'] is not None:
            ret['cur_modalidad'] = int(ret['cur_modalidad'])
        if 'cur_tipo_curso' in ret and ret['cur_tipo_curso'] is not None:
            ret['cur_tipo_curso'] = int(ret['cur_tipo_curso'])
        if 'cur_estado' in ret and ret['cur_estado'] is not None:
            ret['cur_estado'] = int(ret['cur_estado'])
        return ret


class CursoMantenedorSerializer(serializers.ModelSerializer):
    """
    Serializer optimizado para la tabla principal de Cursos (Listado).
    Solo incluye los datos básicos que se muestran en el Data-Table.
    """
    fechas = CursoFechaSerializer(many=True, read_only=True, source='curso_fecha_set')

    class Meta:
        model = Curso
        fields = (
            'cur_id', 'cur_descripcion', 'cur_codigo', 'tcu_id',
            'per_id_responsable', 'car_id_responsable', 'cur_estado',
            'fechas'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convertir IDs a enteros
        for key in ['cur_id', 'tcu_id', 'per_id_responsable', 'car_id_responsable', 'cur_estado']:
            if key in ret and ret[key] is not None:
                ret[key] = int(ret[key])
        return ret