from django.core.management.base import BaseCommand
from django.db import transaction
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.mantenedor_model import Estado_Civil, Comuna, Provincia, Region, Zona, Distrito, Grupo, Rol, Cargo, Nivel, Rama
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Generate test data for the system"

    def handle(self, *args, **kwargs):
        fake = Faker('es_CL')
        
        self.stdout.write("Starting data generation...")
        
        with transaction.atomic():
            self.create_locations(fake)
            self.create_basic_attributes()
            self.create_users_and_personas(fake)
            
        self.stdout.write(self.style.SUCCESS("Data generation completed successfully!"))

    def create_locations(self, fake):
        self.stdout.write("Creating locations...")
        
        # Region
        region, _ = Region.objects.get_or_create(
            reg_descripcion='Biobío',
            defaults={'reg_vigente': True}
        )
        
        # Provincia
        provincia, _ = Provincia.objects.get_or_create(
            pro_descripcion='Concepción',
            reg_id=region,
            defaults={'pro_vigente': True}
        )
        
        # Comunas
        comunas_names = ['Concepción', 'Talcahuano', 'San Pedro de la Paz', 'Chiguayante']
        for name in comunas_names:
            Comuna.objects.get_or_create(
                com_descripcion=name,
                pro_id=provincia,
                defaults={'com_vigente': True}
            )

    def create_basic_attributes(self):
        self.stdout.write("Creating basic attributes (Estado Civil, etc)...")
        
        # Estado Civil
        estados = ['Soltero/a', 'Casado/a', 'Viudo/a', 'Divorciado/a']
        for est in estados:
            Estado_Civil.objects.get_or_create(
                esc_descripcion=est,
                defaults={'esc_vigente': True}
            )
            
        # Zonas
        zonas = ['Zona Biobío Centro', 'Zona Biobío Costa']
        for z in zonas:
            Zona.objects.get_or_create(
                zon_descripcion=z,
                defaults={'zon_vigente': True}
            )
            
        # Distritos
        zona = Zona.objects.first()
        distritos = ['Distrito Concepción', 'Distrito Talcahuano']
        for d in distritos:
            Distrito.objects.get_or_create(
                dis_descripcion=d,
                zon_id=zona,
                defaults={'dis_vigente': True}
            )

    def create_users_and_personas(self, fake):
        self.stdout.write("Creating Users and Personas...")
        
        # Ensure we have required foreign keys
        comunas = list(Comuna.objects.filter(com_vigente=True))
        estados_civil = list(Estado_Civil.objects.filter(esc_vigente=True))
        perfil_default, _ = Perfil.objects.get_or_create(
            pel_descripcion='Usuario Standard', 
            defaults={'pel_vigente': True}
        )
        
        if not comunas or not estados_civil:
            self.stdout.write(self.style.ERROR("Missing Comunas or Estado Civil"))
            return

        for _ in range(10):  # Generate 10 random users
            # User Data
            username = fake.user_name()
            # Ensure unique username
            while Usuario.objects.filter(usu_username=username).exists():
                username = fake.user_name() + str(random.randint(1, 999))
                
            password = 'password123'
            
            user = Usuario.objects.create_user(
                usu_username=username,
                password=password,
                pel_id=perfil_default,
                usu_email=fake.email(),
                usu_vigente=True
            )
            
            # Persona Data
            rut_raw = fake.unique.rut()
            # simple split for rut and dv if formatted like 12.345.678-9 or 12345678-9
            rut_clean = rut_raw.replace('.', '').replace('-', '')
            run = rut_clean[:-1]
            dv = rut_clean[-1]
            
            Persona.objects.create(
                esc_id=random.choice(estados_civil),
                com_id=random.choice(comunas),
                usu_id=user,
                per_run=run[:9], # Enforce max len
                per_dv=dv,
                per_apelpta=fake.last_name(),
                per_apelmat=fake.last_name(),
                per_nombres=fake.first_name(),
                per_mail=user.usu_email,
                per_fecha_nac=fake.date_of_birth(minimum_age=18, maximum_age=80),
                per_direccion=fake.address(),
                per_tipo_fono=random.randint(1, 4),
                per_fono=fake.phone_number()[:15],
                per_apodo=fake.first_name(),
                per_vigente=True
            )
            
        self.stdout.write(f"Created 10 users with their personas.")
