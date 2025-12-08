"""
Test suite for Django models
Testing model creation, validation, and relationships
"""
from django.test import TestCase
from django.db import IntegrityError
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil, Aplicacion, Perfil_Aplicacion
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.curso_model import Curso, Tipo_Curso
from ApiCoreScouts.Models.pago_model import Proveedor, Pago_Persona
from ApiCoreScouts.Models.mantenedor_model import (
    Estado_Civil, Comuna, Region, Grupo, Cargo, Provincia
)
from decimal import Decimal
from datetime import datetime, timezone


class UsuarioModelTest(TestCase):
    """Test cases for Usuario model"""
    
    def setUp(self):
        """Set up test dependencies"""
        self.perfil = Perfil.objects.create(
            pel_descripcion='Test Perfil',
            pel_vigente=True
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
            pel_descripcion='Administrador',
            pel_vigente=True
        )
        self.assertEqual(perfil.pel_descripcion, 'Administrador')
        self.assertTrue(perfil.pel_vigente)
    
    def test_perfil_aplicacion_relationship(self):
        """Test Perfil-Aplicacion many-to-many relationship"""
        perfil = Perfil.objects.create(
            pel_descripcion='Test Perfil',
            pel_vigente=True
        )
        app1 = Aplicacion.objects.create(
            apl_descripcion='Usuarios',
            apl_vigente=True
        )
        app2 = Aplicacion.objects.create(
            apl_descripcion='Personas',
            apl_vigente=True
        )
        
        Perfil_Aplicacion.objects.create(
            pel_id=perfil,
            apl_id=app1,
            pea_consultar=True,
            pea_ingresar=False,
            pea_modificar=False,
            pea_eliminar=False
        )
        Perfil_Aplicacion.objects.create(
            pel_id=perfil,
            apl_id=app2,
            pea_consultar=True,
            pea_ingresar=True,
            pea_modificar=True,
            pea_eliminar=False
        )
        
        # Check relationships
        perfil_apps = Perfil_Aplicacion.objects.filter(pel_id=perfil)
        self.assertEqual(perfil_apps.count(), 2)


class ProveedorModelTest(TestCase):
    """Test cases for Proveedor model"""
    
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


class MantenedorModelTest(TestCase):
    """Test cases for mantenedor models"""
    
    def test_create_estado_civil(self):
        """Test creating Estado_Civil"""
        estado = Estado_Civil.objects.create(
            esc_descripcion='Soltero',
            esc_vigente=True
        )
        self.assertEqual(estado.esc_descripcion, 'Soltero')
        self.assertTrue(estado.esc_vigente)
    
    def test_create_region(self):
        """Test creating Region"""
        region = Region.objects.create(
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.assertEqual(region.reg_descripcion, 'Biobío')
        self.assertTrue(region.reg_vigente)
    
    def test_create_cargo(self):
        """Test creating Cargo"""
        cargo = Cargo.objects.create(
            car_descripcion='Coordinador',
            car_vigente=True
        )
        self.assertEqual(cargo.car_descripcion, 'Coordinador')
        self.assertTrue(cargo.car_vigente)

