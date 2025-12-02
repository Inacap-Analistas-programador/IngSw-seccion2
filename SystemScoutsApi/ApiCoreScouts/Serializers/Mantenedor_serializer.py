from rest_framework import serializers
from ..Models.mantenedor_model import *

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'rol_id' in ret and ret['rol_id'] is not None:
            ret['rol_id'] = int(ret['rol_id'])
        if 'rol_tipo' in ret and ret['rol_tipo'] is not None:
            ret['rol_tipo'] = int(ret['rol_tipo'])
        return ret

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'car_id' in ret and ret['car_id'] is not None:
            ret['car_id'] = int(ret['car_id'])
        return ret

class RamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rama
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'ram_id' in ret and ret['ram_id'] is not None:
            ret['ram_id'] = int(ret['ram_id'])
        return ret

class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Civil
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'esc_id' in ret and ret['esc_id'] is not None:
            ret['esc_id'] = int(ret['esc_id'])
        return ret

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'niv_id' in ret and ret['niv_id'] is not None:
            ret['niv_id'] = int(ret['niv_id'])
        if 'niv_orden' in ret and ret['niv_orden'] is not None:
            ret['niv_orden'] = int(ret['niv_orden'])
        return ret

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'zon_id' in ret and ret['zon_id'] is not None:
            ret['zon_id'] = int(ret['zon_id'])
        return ret

class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'dis_id' in ret and ret['dis_id'] is not None:
            ret['dis_id'] = int(ret['dis_id'])
        if 'zon_id' in ret and ret['zon_id'] is not None:
            ret['zon_id'] = int(ret['zon_id'])
        return ret

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'gru_id' in ret and ret['gru_id'] is not None:
            ret['gru_id'] = int(ret['gru_id'])
        if 'dis_id' in ret and ret['dis_id'] is not None:
            ret['dis_id'] = int(ret['dis_id'])
        return ret

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'reg_id' in ret and ret['reg_id'] is not None:
            ret['reg_id'] = int(ret['reg_id'])
        return ret

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'pro_id' in ret and ret['pro_id'] is not None:
            ret['pro_id'] = int(ret['pro_id'])
        if 'reg_id' in ret and ret['reg_id'] is not None:
            ret['reg_id'] = int(ret['reg_id'])
        return ret

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'com_id' in ret and ret['com_id'] is not None:
            ret['com_id'] = int(ret['com_id'])
        if 'pro_id' in ret and ret['pro_id'] is not None:
            ret['pro_id'] = int(ret['pro_id'])
        return ret

class AlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimentacion
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'ali_id' in ret and ret['ali_id'] is not None:
            ret['ali_id'] = int(ret['ali_id'])
        if 'ali_tipo' in ret and ret['ali_tipo'] is not None:
            ret['ali_tipo'] = int(ret['ali_tipo'])
        return ret

class ConceptoContableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepto_Contable
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'coc_id' in ret and ret['coc_id'] is not None:
            ret['coc_id'] = int(ret['coc_id'])
        return ret

class TipoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Curso
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'tcu_id' in ret and ret['tcu_id'] is not None:
            ret['tcu_id'] = int(ret['tcu_id'])
        if 'tcu_tipo' in ret and ret['tcu_tipo'] is not None:
            ret['tcu_tipo'] = int(ret['tcu_tipo'])
        if 'tcu_cant_participante' in ret and ret['tcu_cant_participante'] is not None:
            ret['tcu_cant_participante'] = int(ret['tcu_cant_participante'])
        return ret

class TipoArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Archivo
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'tar_id' in ret and ret['tar_id'] is not None:
            ret['tar_id'] = int(ret['tar_id'])
        return ret