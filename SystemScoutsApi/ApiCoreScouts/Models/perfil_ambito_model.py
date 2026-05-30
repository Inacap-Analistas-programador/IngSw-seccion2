from django.db import models
from django.contrib.auth.models import Group

# ── Constantes de nivel de ámbito ─────────────────────────────────────────
NIVEL_GRUPO    = 1   # Solo un grupo específico dentro de distrito y zona
NIVEL_DISTRITO = 2   # Todo un distrito dentro de una zona
NIVEL_ZONA     = 3   # Toda una zona (todos sus distritos)
NIVEL_GLOBAL   = 4   # Sin restricciones (acceso total)

NIVEL_CHOICES = [
    (NIVEL_GRUPO,    'Grupo (Restricto)'),
    (NIVEL_DISTRITO, 'Distrito'),
    (NIVEL_ZONA,     'Zona'),
    (NIVEL_GLOBAL,   'Global'),
]


class PerfilAmbito(models.Model):
    """
    Extiende el Group de Django (Perfil) con restricciones de ámbito geográfico.
    Actúa como filtro de datos para todas las consultas: determina QUÉ FILAS
    puede ver el usuario, complementando los permisos CRUD que determinan
    QUÉ OPERACIONES puede realizar.

    Nivel 4 – Global   : Sin restricciones (ve toda la información del sistema)
    Nivel 3 – Zona     : Solo datos de una zona específica
    Nivel 2 – Distrito : Solo datos de un distrito + zona
    Nivel 1 – Grupo    : Solo datos de un grupo + distrito + zona
    """
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='ambito',
        verbose_name='Perfil'
    )
    nivel = models.IntegerField(
        choices=NIVEL_CHOICES,
        default=NIVEL_GLOBAL,
        verbose_name='Nivel de Acceso',
        db_column='pam_nivel'
    )
    # FKs opcionales — se rellenan según el nivel requerido
    zona = models.ForeignKey(
        'Zona',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ambitos',
        db_column='pam_zon_id',
        verbose_name='Zona',
    )
    distrito = models.ForeignKey(
        'Distrito',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ambitos',
        db_column='pam_dis_id',
        verbose_name='Distrito',
    )
    grupo = models.ForeignKey(
        'Grupo',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ambitos',
        db_column='pam_gru_id',
        verbose_name='Grupo',
    )

    class Meta:
        db_table = 'perfil_ambito'
        verbose_name = 'Ámbito de Perfil'
        verbose_name_plural = 'Ámbitos de Perfil'

    # ── Validación de coherencia jerárquica ───────────────────────────────
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.nivel == NIVEL_GLOBAL:
            if self.zona_id or self.distrito_id or self.grupo_id:
                raise ValidationError(
                    "Nivel Global no debe tener zona, distrito ni grupo asignados."
                )

        elif self.nivel == NIVEL_ZONA:
            if not self.zona_id:
                raise ValidationError("Nivel Zona requiere una zona definida.")
            if self.distrito_id or self.grupo_id:
                raise ValidationError(
                    "Nivel Zona no debe tener distrito ni grupo asignados."
                )

        elif self.nivel == NIVEL_DISTRITO:
            if not self.zona_id or not self.distrito_id:
                raise ValidationError(
                    "Nivel Distrito requiere zona y distrito definidos."
                )
            if self.grupo_id:
                raise ValidationError(
                    "Nivel Distrito no debe tener grupo asignado."
                )
            # Validar FK: el distrito pertenece a la zona indicada
            if self.distrito and self.distrito.zon_id_id != self.zona_id:
                raise ValidationError(
                    f"El distrito '{self.distrito}' no pertenece a la zona indicada."
                )

        elif self.nivel == NIVEL_GRUPO:
            if not self.zona_id or not self.distrito_id or not self.grupo_id:
                raise ValidationError(
                    "Nivel Grupo requiere zona, distrito y grupo definidos."
                )
            # Validar FK grupo → distrito → zona
            if self.grupo and self.grupo.dis_id_id != self.distrito_id:
                raise ValidationError(
                    f"El grupo '{self.grupo}' no pertenece al distrito indicado."
                )
            if self.distrito and self.distrito.zon_id_id != self.zona_id:
                raise ValidationError(
                    f"El distrito '{self.distrito}' no pertenece a la zona indicada."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def to_jwt_payload(self) -> dict:
        """Retorna un diccionario listo para embeber en el JWT."""
        return {
            'nivel':       self.nivel,
            'zona_id':     self.zona_id,
            'distrito_id': self.distrito_id,
            'grupo_id':    self.grupo_id,
        }

    def __str__(self):
        nivel_display = dict(NIVEL_CHOICES).get(self.nivel, self.nivel)
        return f"{self.group.name} – {nivel_display}"
