"""
Test suite for Django models
Testing model creation, validation, and relationships
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil, Aplicacion, Perfil_Aplicacion
from ApiCoreScouts.Models.persona_model import Persona, Persona_Grupo
from ApiCoreScouts.Models.curso_model import Curso, Tipo_Curso
from ApiCoreScouts.Models.pago_model import Proveedor, Comprobante_Pago, Pago_Persona
from ApiCoreScouts.Models.mantenedor_model import (
    Estado_Civil, Comuna, Region, Pais, Grupo, Cargo, Concepto_Contable
)
from decimal import Decimal
from datetime import datetime, timezone


class UsuarioModelTest(TestCase):
    """Test cases for Usuario model"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Test Perfil',
            PEL_VIGENTE=True
        )
    
    def test_create_usuario(self):
        """Test creating a new Usuario"""
        usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil
        )
        self.assertEqual(usuario.usu_username, 'testuser')
        self.assertTrue(usuario.check_password('testpass123'))
        self.assertTrue(usuario.is_active)
        self.assertFalse(usuario.is_staff)
    
    def test_usuario_unique_username(self):
        """Test that username must be unique"""
        Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil
        )
        with self.assertRaises(IntegrityError):
            Usuario.objects.create_user(
                usu_username='testuser',
                password='anotherpass',
                pel_id=self.perfil
            )
    
    def test_usuario_password_hashing(self):
        """Test that passwords are properly hashed"""
        usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='mypassword',
            pel_id=self.perfil
        )
        # Password should not be stored in plain text
        self.assertNotEqual(usuario.password, 'mypassword')
        # But check_password should work
        self.assertTrue(usuario.check_password('mypassword'))
        self.assertFalse(usuario.check_password('wrongpassword'))


class PerfilModelTest(TestCase):
    """Test cases for Perfil model"""
    
    def test_create_perfil(self):
        """Test creating a new Perfil"""
        perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Administrador',
            PEL_VIGENTE=True
        )
        self.assertEqual(perfil.PEL_DESCRIPCION, 'Administrador')
        self.assertTrue(perfil.PEL_VIGENTE)
    
    def test_perfil_aplicacion_relationship(self):
        """Test Perfil-Aplicacion many-to-many relationship"""
        perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Test Perfil',
            PEL_VIGENTE=True
        )
        app1 = Aplicacion.objects.create(
            APL_DESCRIPCION='Usuarios',
            APL_ICONO='user-icon',
            APL_VIGENTE=True
        )
        app2 = Aplicacion.objects.create(
            APL_DESCRIPCION='Personas',
            APL_ICONO='person-icon',
            APL_VIGENTE=True
        )
        
        Perfil_Aplicacion.objects.create(
            PEL_ID=perfil,
            APL_ID=app1,
            PAP_VER=True,
            PAP_EDITAR=False,
            PAP_ELIMINAR=False,
            PAP_VIGENTE=True
        )
        Perfil_Aplicacion.objects.create(
            PEL_ID=perfil,
            APL_ID=app2,
            PAP_VER=True,
            PAP_EDITAR=True,
            PAP_ELIMINAR=False,
            PAP_VIGENTE=True
        )
        
        # Check relationships
        perfil_apps = Perfil_Aplicacion.objects.filter(PEL_ID=perfil, PAP_VIGENTE=True)
        self.assertEqual(perfil_apps.count(), 2)


class PersonaModelTest(TestCase):
    """Test cases for Persona model"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Test Perfil',
            PEL_VIGENTE=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil
        )
        self.pais = Pais.objects.create(
            pai_descripcion='Chile',
            pai_vigente=True
        )
        self.region = Region.objects.create(
            pai_id=self.pais,
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.comuna = Comuna.objects.create(
            reg_id=self.region,
            com_descripcion='Concepción',
            com_vigente=True
        )
        self.estado_civil = Estado_Civil.objects.create(
            esc_descripcion='Soltero',
            esc_vigente=True
        )
    
    def test_create_persona(self):
        """Test creating a new Persona"""
        persona = Persona.objects.create(
            esc_id=self.estado_civil,
            com_id=self.comuna,
            usu_id=self.usuario,
            per_run='12345678',
            per_dv='9',
            per_apelpta='González',
            per_apelmat='López',
            per_nombres='Juan Pablo',
            per_mail='juan@example.com',
            per_fecha_nac=datetime(1990, 5, 15, tzinfo=timezone.utc),
            per_direccion='Calle Principal 123',
            per_tipo_fono=2,
            per_fono='+56912345678',
            per_apodo='Juanito',
            per_vigente=True
        )
        self.assertEqual(persona.per_run, '12345678')
        self.assertEqual(persona.per_nombres, 'Juan Pablo')
        self.assertTrue(persona.per_vigente)
    
    def test_persona_unique_run(self):
        """Test that RUN must be unique"""
        Persona.objects.create(
            esc_id=self.estado_civil,
            com_id=self.comuna,
            usu_id=self.usuario,
            per_run='12345678',
            per_dv='9',
            per_apelpta='González',
            per_nombres='Juan',
            per_mail='juan@example.com',
            per_fecha_nac=datetime(1990, 5, 15, tzinfo=timezone.utc),
            per_direccion='Calle Principal 123',
            per_tipo_fono=2,
            per_fono='+56912345678',
            per_apodo='Juanito',
            per_vigente=True
        )
        with self.assertRaises(IntegrityError):
            Persona.objects.create(
                esc_id=self.estado_civil,
                com_id=self.comuna,
                usu_id=self.usuario,
                per_run='12345678',  # Duplicate RUN
                per_dv='9',
                per_apelpta='Pérez',
                per_nombres='María',
                per_mail='maria@example.com',
                per_fecha_nac=datetime(1995, 3, 20, tzinfo=timezone.utc),
                per_direccion='Otra Calle 456',
                per_tipo_fono=2,
                per_fono='+56987654321',
                per_apodo='Mary',
                per_vigente=True
            )


class CursoModelTest(TestCase):
    """Test cases for Curso model"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Test Perfil',
            PEL_VIGENTE=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil
        )
        self.pais = Pais.objects.create(
            pai_descripcion='Chile',
            pai_vigente=True
        )
        self.region = Region.objects.create(
            pai_id=self.pais,
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.comuna = Comuna.objects.create(
            reg_id=self.region,
            com_descripcion='Concepción',
            com_vigente=True
        )
        self.estado_civil = Estado_Civil.objects.create(
            esc_descripcion='Soltero',
            esc_vigente=True
        )
        self.persona = Persona.objects.create(
            esc_id=self.estado_civil,
            com_id=self.comuna,
            usu_id=self.usuario,
            per_run='12345678',
            per_dv='9',
            per_apelpta='González',
            per_nombres='Juan',
            per_mail='juan@example.com',
            per_fecha_nac=datetime(1990, 5, 15, tzinfo=timezone.utc),
            per_direccion='Calle Principal 123',
            per_tipo_fono=2,
            per_fono='+56912345678',
            per_apodo='Juanito',
            per_vigente=True
        )
        self.cargo = Cargo.objects.create(
            car_descripcion='Coordinador',
            car_vigente=True
        )
        self.tipo_curso = Tipo_Curso.objects.create(
            tcu_descripcion='Formación',
            tcu_vigente=True
        )
    
    def test_create_curso(self):
        """Test creating a new Curso"""
        curso = Curso.objects.create(
            usu_id=self.usuario,
            tcu_id=self.tipo_curso,
            per_id_responsable=self.persona,
            car_id_responsable=self.cargo,
            com_id_lugar=self.comuna,
            cur_fecha_solicitud=datetime.now(timezone.utc),
            cur_codigo='CURSO001',
            cur_descripcion='Curso de Formación Scout',
            cur_administra=1,
            cur_cota_con_almuerzo=50000,
            cur_cota_sin_almuerzo=30000,
            cur_modalidad=1,
            cur_tipo_curso=1,
            cur_lugar='Campamento Las Rocas',
            cur_estado=1
        )
        self.assertEqual(curso.cur_codigo, 'CURSO001')
        self.assertEqual(curso.cur_estado, 1)
        self.assertTrue(curso.cur_descripcion)
    
    def test_curso_unique_codigo(self):
        """Test that course code must be unique"""
        Curso.objects.create(
            usu_id=self.usuario,
            tcu_id=self.tipo_curso,
            per_id_responsable=self.persona,
            car_id_responsable=self.cargo,
            com_id_lugar=self.comuna,
            cur_fecha_solicitud=datetime.now(timezone.utc),
            cur_codigo='CURSO001',
            cur_descripcion='Curso 1',
            cur_administra=1,
            cur_cota_con_almuerzo=50000,
            cur_cota_sin_almuerzo=30000,
            cur_modalidad=1,
            cur_tipo_curso=1,
            cur_lugar='Lugar 1',
            cur_estado=1
        )
        with self.assertRaises(IntegrityError):
            Curso.objects.create(
                usu_id=self.usuario,
                tcu_id=self.tipo_curso,
                per_id_responsable=self.persona,
                car_id_responsable=self.cargo,
                com_id_lugar=self.comuna,
                cur_fecha_solicitud=datetime.now(timezone.utc),
                cur_codigo='CURSO001',  # Duplicate code
                cur_descripcion='Curso 2',
                cur_administra=1,
                cur_cota_con_almuerzo=40000,
                cur_cota_sin_almuerzo=25000,
                cur_modalidad=1,
                cur_tipo_curso=1,
                cur_lugar='Lugar 2',
                cur_estado=1
            )


class PagoModelTest(TestCase):
    """Test cases for Pago-related models"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.perfil = Perfil.objects.create(
            PEL_DESCRIPCION='Test Perfil',
            PEL_VIGENTE=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil
        )
        self.pais = Pais.objects.create(
            pai_descripcion='Chile',
            pai_vigente=True
        )
        self.region = Region.objects.create(
            pai_id=self.pais,
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.comuna = Comuna.objects.create(
            reg_id=self.region,
            com_descripcion='Concepción',
            com_vigente=True
        )
        self.estado_civil = Estado_Civil.objects.create(
            esc_descripcion='Soltero',
            esc_vigente=True
        )
        self.persona = Persona.objects.create(
            esc_id=self.estado_civil,
            com_id=self.comuna,
            usu_id=self.usuario,
            per_run='12345678',
            per_dv='9',
            per_apelpta='González',
            per_nombres='Juan',
            per_mail='juan@example.com',
            per_fecha_nac=datetime(1990, 5, 15, tzinfo=timezone.utc),
            per_direccion='Calle Principal 123',
            per_tipo_fono=2,
            per_fono='+56912345678',
            per_apodo='Juanito',
            per_vigente=True
        )
        self.cargo = Cargo.objects.create(
            car_descripcion='Coordinador',
            car_vigente=True
        )
        self.tipo_curso = Tipo_Curso.objects.create(
            tcu_descripcion='Formación',
            tcu_vigente=True
        )
        self.curso = Curso.objects.create(
            usu_id=self.usuario,
            tcu_id=self.tipo_curso,
            per_id_responsable=self.persona,
            car_id_responsable=self.cargo,
            com_id_lugar=self.comuna,
            cur_fecha_solicitud=datetime.now(timezone.utc),
            cur_codigo='CURSO001',
            cur_descripcion='Curso Test',
            cur_administra=1,
            cur_cota_con_almuerzo=50000,
            cur_cota_sin_almuerzo=30000,
            cur_modalidad=1,
            cur_tipo_curso=1,
            cur_lugar='Lugar Test',
            cur_estado=1
        )
    
    def test_create_proveedor(self):
        """Test creating a new Proveedor"""
        proveedor = Proveedor.objects.create(
            prv_descripcion='Proveedor Test S.A.',
            prv_celular1='+56912345678',
            prv_direccion='Av. Principal 100',
            prv_vigente=True
        )
        self.assertEqual(proveedor.prv_descripcion, 'Proveedor Test S.A.')
        self.assertTrue(proveedor.prv_vigente)
    
    def test_create_pago_persona(self):
        """Test creating a new Pago_Persona"""
        pago = Pago_Persona.objects.create(
            per_id=self.persona,
            cur_id=self.curso,
            usu_id=self.usuario,
            pap_fecha_hora=datetime.now(timezone.utc),
            pap_tipo=1,
            pap_valor=Decimal('50000.00')
        )
        self.assertEqual(pago.pap_tipo, 1)
        self.assertEqual(pago.pap_valor, Decimal('50000.00'))
        self.assertEqual(pago.per_id, self.persona)
