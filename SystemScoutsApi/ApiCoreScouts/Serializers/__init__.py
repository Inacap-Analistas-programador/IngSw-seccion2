from .Usuarios_serializers import *
from .Cursos_serializers import *
from .Mantenedores_serializers import *
from .Pagos_serializers import *
from .Archivos_serializers import *
from .Personas_serializers import *

serializers_dict = {
    # USUARIOS y CURSOS
    'Usuario': UsuarioSerializer,
    'Perfil': PerfilSerializer,
    'Persona': PersonaSerializer,
    'Persona_Grupo': PersonaGrupoSerializer,
    'Persona_Formador': PersonaFormadorSerializer,
    'Persona_Curso': PersonaCursoSerializer,
    'Persona_Individual': PersonaIndividualSerializer,
    'Persona_Nivel': PersonaNivelSerializer,
    'Persona_Estado_Curso': PersonaEstadoCursoSerializer,
    'Persona_Vehiculo': PersonaVehiculoSerializer,
    'Curso': CursoSerializer,
    'Tipo_Curso': TipoCursoSerializer,
    'Curso_Cuota': CursoCuotaSerializer,
    'Curso_Fecha': CursoFechaSerializer,
    'Curso_Alimentacion': CursoAlimentacionSerializer,
    'Curso_Coordinador': CursoCoordinadorSerializer,
    'Curso_Seccion': CursoSeccionSerializer,
    'Curso_Formador': CursoFormadorSerializer,

    # ARCHIVOS
    'Archivo': ArchivoSerializer,
    'Archivo_Curso': ArchivoCursoSerializer,
    'Archivo_Persona': ArchivoPersonaSerializer,
    'Tipo_Archivo': TipoArchivoSerializer,

    # MANTENEDORES
    'Rol': RolSerializer,
    'Cargo': CargoSerializer,
    'Rama': RamaSerializer,
    'Estado_Civil': EstadoCivilSerializer,
    'Nivel': NivelSerializer,
    'Zona': ZonaSerializer,
    'Distrito': DistritoSerializer,
    'Grupo': GrupoSerializer,
    'Region': RegionSerializer,
    'Provincia': ProvinciaSerializer,
    'Comuna': ComunaSerializer,

    # PAGOS
    'Concepto_Contable': ConceptoContableSerializer,
    'Proveedor': ProveedorSerializer,
}
