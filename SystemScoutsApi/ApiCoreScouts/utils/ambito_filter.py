"""
ambito_filter.py
Utilidad para filtrar QuerySets según el ámbito geográfico del usuario autenticado.

USO:
    from ApiCoreScouts.utils.ambito_filter import get_ambito_from_user, filtrar_por_ambito

    def get_queryset(self):
        ambito = get_ambito_from_user(self.request.user)
        return filtrar_por_ambito(MiModelo.objects.all(), ambito, ...)
"""
from ..Models.perfil_ambito_model import NIVEL_GLOBAL, NIVEL_ZONA, NIVEL_DISTRITO, NIVEL_GRUPO


def get_ambito_from_user(user) -> dict | None:
    """
    Extrae el ámbito del primer perfil (Group) que tenga PerfilAmbito asignado.
    Retorna None si el usuario es superuser o si su nivel es GLOBAL (sin restricción).
    Retorna un dict con: { 'nivel', 'zona', 'distrito', 'grupo' } si hay restricción.
    """
    if user.is_superuser or not user.is_authenticated:
        return None  # Sin restricción

    for group in user.groups.select_related('ambito').all():
        try:
            amb = group.ambito
            if amb.nivel == NIVEL_GLOBAL:
                return None  # Perfil global → sin filtro
            return {
                'nivel':    amb.nivel,
                'zona':     amb.zona_id,
                'distrito': amb.distrito_id,
                'grupo':    amb.grupo_id,
            }
        except Exception:
            continue  # Este grupo no tiene PerfilAmbito

    return None  # Sin PerfilAmbito configurado → acceso global por defecto


def filtrar_por_ambito(
    queryset,
    ambito: dict | None,
    campo_zona: str      = 'gru_id__dis_id__zon_id',
    campo_distrito: str  = 'gru_id__dis_id',
    campo_grupo: str     = 'gru_id',
):
    """
    Aplica el filtro de ámbito a cualquier queryset que tenga relación con
    la jerarquía Zona → Distrito → Grupo.

    Parámetros:
        queryset      – QuerySet de Django a filtrar.
        ambito        – Dict devuelto por get_ambito_from_user(), o None.
        campo_zona    – Lookup field hacia Zona (soporta relaciones traversales).
        campo_distrito– Lookup field hacia Distrito.
        campo_grupo   – Lookup field hacia Grupo.

    Retorna el queryset con el filtro aplicado, o el original si ambito es None.
    """
    if ambito is None:
        return queryset  # Global → sin filtro

    nivel = ambito['nivel']

    if nivel == NIVEL_ZONA:
        return queryset.filter(**{campo_zona: ambito['zona']})

    elif nivel == NIVEL_DISTRITO:
        return queryset.filter(**{campo_distrito: ambito['distrito']})

    elif nivel == NIVEL_GRUPO:
        return queryset.filter(**{campo_grupo: ambito['grupo']})

    return queryset  # Fallback: sin filtro


# ── Helpers de ámbito específicos por dominio ─────────────────────────────

def filtrar_personas_por_ambito(queryset, ambito: dict | None):
    """
    Filtra el modelo Persona teniendo en cuenta que la relación con Grupo
    va a través de Persona_Grupo (many) o Persona_Individual (con zona/distrito).
    Se filtra por la membresía de grupo activa (persona_grupo).
    """
    if ambito is None:
        return queryset

    nivel = ambito['nivel']

    if nivel == NIVEL_GRUPO:
        return queryset.filter(
            persona_grupo__gru_id=ambito['grupo'],
            persona_grupo__peg_vigente=True
        )
    elif nivel == NIVEL_DISTRITO:
        return queryset.filter(
            persona_grupo__gru_id__dis_id=ambito['distrito'],
            persona_grupo__peg_vigente=True
        )
    elif nivel == NIVEL_ZONA:
        return queryset.filter(
            persona_grupo__gru_id__dis_id__zon_id=ambito['zona'],
            persona_grupo__peg_vigente=True
        )

    return queryset


def filtrar_cursos_por_ambito(queryset, ambito: dict | None):
    """
    Filtra Curso/CursoSeccion por el campo gru_id que tienen en la seccion.
    """
    return filtrar_por_ambito(
        queryset, ambito,
        campo_zona='gru_id__dis_id__zon_id',
        campo_distrito='gru_id__dis_id',
        campo_grupo='gru_id',
    )
