from rest_framework import serializers

from ModuloUsuarioCurso.models import (Aplicacion, Perfil_Aplicacion, Usuario, Perfil, Persona_Curso, Persona, Persona_Grupo, Persona_Formador, Persona_Individual, Persona_Nivel, Persona_Estado_Curso, Persona_Vehiculo,Curso, Tipo_Curso,  Curso_Cuota, Curso_Fecha, Curso_Alimentacion, Curso_Coordinador, Curso_Seccion, Curso_Formador)
from ModuloArchivos.models import (Archivo, Archivo_Curso, Archivo_Persona, Tipo_Archivo)
from ModuloMantenedores.models import (Alimentacion, Rol, Cargo, Rama, Estado_Civil, Nivel, Zona, Distrito, Grupo, Region, Provincia, Comuna)
from ModuloPagos.models import (Comprobante_Pago, Concepto_Contable, Pago_Comprobante, Pago_Persona, Prepago, Proveedor)

# ======================================================
# MÓDULO USUARIOS
# ======================================================
class ModuloUsuarioCursoSerializers:
    class UsuarioSerializer(serializers.ModelSerializer):
        class Meta:
            model = Usuario
            fields = '__all__'


    class AplicacionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Aplicacion
            fields = '__all__'
            
    class PerfilSerializer(serializers.ModelSerializer):
        class Meta:
            model = Perfil
            fields = '__all__'


    class PersonaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Persona
            fields = '__all__'


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

    class CursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Curso
            fields = '__all__'

    class PersonaCursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Persona_Curso
            fields = '__all__'

    class PersonaEstadoCursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Persona_Estado_Curso
            fields = '__all__'


    class PersonaVehiculoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Persona_Vehiculo
            fields = '__all__'

    class PerfilAplicacionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Perfil_Aplicacion
            fields = '__all__'

    class TipoCursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tipo_Curso
            fields = '__all__'


    class CursoCuotaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Curso_Cuota
            fields = '__all__'


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
        class Meta:
            model = Curso_Seccion
            fields = '__all__'


    class CursoFormadorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Curso_Formador
            fields = '__all__'

# ======================================================
# MÓDULO ARCHIVOS
# ======================================================
class ModuloArchivosSerializers:
    class ArchivoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Archivo
            fields = '__all__'


    class ArchivoCursoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Archivo_Curso
            fields = '__all__'


    class ArchivoPersonaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Archivo_Persona
            fields = '__all__'


    class TipoArchivoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tipo_Archivo
            fields = '__all__'

# ======================================================
# MÓDULO MANTENEDORES
# ======================================================
class ModuloMantenedoresSerializers:
    class RolSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rol
            fields = '__all__'


    class CargoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cargo
            fields = '__all__'


    class RamaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rama
            fields = '__all__'


    class EstadoCivilSerializer(serializers.ModelSerializer):
        class Meta:
            model = Estado_Civil
            fields = '__all__'


    class NivelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Nivel
            fields = '__all__'


    class ZonaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Zona
            fields = '__all__'


    class DistritoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Distrito
            fields = '__all__'


    class GrupoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Grupo
            fields = '__all__'


    class RegionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Region
            fields = '__all__'


    class ProvinciaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Provincia
            fields = '__all__'


    class ComunaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comuna
            fields = '__all__'

    class AlimentacionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Alimentacion
            fields = '__all__' 
# ======================================================
# MÓDULO PAGOS  
# ======================================================
class ModuloPagosSerializers:
    class ProveedorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Proveedor
            fields = '__all__'

    class ConceptoContableSerializer(serializers.ModelSerializer):
        class Meta:
            model = Concepto_Contable
            fields = '__all__'

    class ComprobantePagoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comprobante_Pago
            fields = '__all__'
        
    class PagoComprobanteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Pago_Comprobante
            fields = '__all__'
        
    class PagoPersonaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Pago_Persona
            fields = '__all__'
        
    class PrepagoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Prepago
            fields = '__all__'
        
    
# ======================================================
# DICCIONARIO DE SERIALIZERS PARA DynamicModelViewSet
# ======================================================
serializers_dict = {
    # ==========================================
    # USUARIOS y CURSOS
    # ==========================================
    'Usuario': ModuloUsuarioCursoSerializers.UsuarioSerializer,
    'Perfil': ModuloUsuarioCursoSerializers.PerfilSerializer,
    'Persona': ModuloUsuarioCursoSerializers.PersonaSerializer,
    'Persona_Grupo': ModuloUsuarioCursoSerializers.PersonaGrupoSerializer,
    'Persona_Formador': ModuloUsuarioCursoSerializers.PersonaFormadorSerializer,
    'Persona_Curso': ModuloUsuarioCursoSerializers.PersonaCursoSerializer,
    'Persona_Individual': ModuloUsuarioCursoSerializers.PersonaIndividualSerializer,
    'Persona_Nivel': ModuloUsuarioCursoSerializers.PersonaNivelSerializer,
    'Persona_Estado_Curso': ModuloUsuarioCursoSerializers.PersonaEstadoCursoSerializer,
    'Persona_Vehiculo': ModuloUsuarioCursoSerializers.PersonaVehiculoSerializer,
    'Curso': ModuloUsuarioCursoSerializers.CursoSerializer,
    'Tipo_Curso': ModuloUsuarioCursoSerializers.TipoCursoSerializer,
    'Curso_Cuota': ModuloUsuarioCursoSerializers.CursoCuotaSerializer,
    'Curso_Fecha': ModuloUsuarioCursoSerializers.CursoFechaSerializer,
    'Curso_Alimentacion': ModuloUsuarioCursoSerializers.CursoAlimentacionSerializer,
    'Curso_Coordinador': ModuloUsuarioCursoSerializers.CursoCoordinadorSerializer,
    'Curso_Seccion': ModuloUsuarioCursoSerializers.CursoSeccionSerializer,
    'Curso_Formador': ModuloUsuarioCursoSerializers.CursoFormadorSerializer,

    # ==========================================
    # ARCHIVOS
    # ==========================================
    'Archivo': ModuloArchivosSerializers.ArchivoSerializer,
    'Archivo_Curso': ModuloArchivosSerializers.ArchivoCursoSerializer,
    'Archivo_Persona': ModuloArchivosSerializers.ArchivoPersonaSerializer,
    'Tipo_Archivo': ModuloArchivosSerializers.TipoArchivoSerializer,

    # ==========================================
    # MANTENEDORES
    # ==========================================
    'Rol': ModuloMantenedoresSerializers.RolSerializer,
    'Cargo': ModuloMantenedoresSerializers.CargoSerializer,
    'Rama': ModuloMantenedoresSerializers.RamaSerializer,
    'Estado_Civil': ModuloMantenedoresSerializers.EstadoCivilSerializer,
    'Nivel': ModuloMantenedoresSerializers.NivelSerializer,
    'Zona': ModuloMantenedoresSerializers.ZonaSerializer,
    'Distrito': ModuloMantenedoresSerializers.DistritoSerializer,
    'Grupo': ModuloMantenedoresSerializers.GrupoSerializer,
    'Region': ModuloMantenedoresSerializers.RegionSerializer,
    'Provincia': ModuloMantenedoresSerializers.ProvinciaSerializer,
    'Comuna': ModuloMantenedoresSerializers.ComunaSerializer,

    # ==========================================
    # PAGOS
    # ==========================================
    'Concepto_Contable': ModuloPagosSerializers.ConceptoContableSerializer,
    'Proveedor': ModuloPagosSerializers.ProveedorSerializer,
}

