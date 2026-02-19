from django.core.management.base import BaseCommand
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.usuario_model import Usuario
from django.db import transaction

class Command(BaseCommand):
    help = 'Updates email for a specific user/person'

    def handle(self, *args, **kwargs):
        old_email = 'juan@scouts.cl'
        new_email = 'helloworld.gogam@gmail.com'
        
        self.stdout.write(f"Attempting to change email from {old_email} to {new_email}...")

        try:
            with transaction.atomic():
                # 1. Update Persona
                personas = Persona.objects.filter(per_mail=old_email)
                persona_count = personas.count()
                
                if persona_count > 0:
                    self.stdout.write(f"Found {persona_count} Persona(s) with email {old_email}")
                    for persona in personas:
                        persona.per_mail = new_email
                        persona.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated Persona: {persona.per_nombres} {persona.per_apelpta} (ID: {persona.per_id})"))
                        
                        # Update linked user if exists
                        if persona.usu_id:
                            usuario = persona.usu_id
                            if usuario.usu_email != new_email:
                                usuario.usu_email = new_email
                                usuario.save()
                                self.stdout.write(self.style.SUCCESS(f"Updated linked Usuario: {usuario.usu_username} (ID: {usuario.usu_id})"))
                else:
                    self.stdout.write(self.style.WARNING(f"No Persona found with email {old_email}"))

                # 2. Update Usuario (if not already updated via Persona or if standalone)
                usuarios = Usuario.objects.filter(usu_email=old_email)
                usuario_count = usuarios.count()

                if usuario_count > 0:
                    self.stdout.write(f"Found {usuario_count} Useario(s) with email {old_email}")
                    for usuario in usuarios:
                        usuario.usu_email = new_email
                        usuario.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated Usuario: {usuario.usu_username} (ID: {usuario.usu_id})"))
                else:
                    if persona_count == 0:
                         self.stdout.write(self.style.WARNING(f"No Usuario found with email {old_email} either."))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error updating email: {str(e)}"))
