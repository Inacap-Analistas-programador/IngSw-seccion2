
from django.db import models
from django.conf import settings

# modelo para guardar los logs de seguridad
class SL(models.Model):
    # tipos de eventos que vamos a registrar
    ETS = [
        ('LOGIN_SUCCESS', 'Login Exitoso'),
        ('LOGIN_FAIL', 'Login Fallido'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('PASSWORD_CHANGE', 'Cambio de Contraseña'),
        ('UNAUTHORIZED_ACCESS', 'Acceso No Autorizado'),
        ('SUSPICIOUS_ACTIVITY', 'Actividad Sospechosa'),
        ('API_MOD', 'Modificación API'),
    ]

    id = models.BigAutoField(primary_key=True)
    # usuario que hizo la accion, puede ser null si no se logueo
    us = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sls'
    )
    et = models.CharField(max_length=50, choices=ETS)
    ip = models.GenericIPAddressField(null=True, blank=True)
    ts = models.DateTimeField(auto_now_add=True)
    dt = models.TextField(null=True, blank=True)
    ua = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'sl'
        ordering = ['-ts']
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        return f"{self.ts} - {self.et} - {self.us}"
