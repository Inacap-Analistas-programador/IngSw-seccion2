from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Heredamos: password, last_login, is_superuser, username, first_name, 
    # last_name, email, is_staff, is_active, date_joined.
    
    # Mantenemos usu_id como primary key para compatibilidad con relaciones existentes
    usu_id = models.BigAutoField(primary_key=True, db_column='usu_id')
    
    # Campo personalizado adicional
    usu_ruta_foto = models.CharField(max_length=255, null=True, db_column='usu_ruta_foto')

    @property
    def id(self):
        return self.usu_id

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.username