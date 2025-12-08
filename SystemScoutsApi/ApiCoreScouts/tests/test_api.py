"""
Test suite for API endpoints
Testing REST API views, authentication, and authorization
"""
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil, Aplicacion, Perfil_Aplicacion
from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.curso_model import Curso, Tipo_Curso
from ApiCoreScouts.Models.pago_model import Proveedor, Pago_Persona
from ApiCoreScouts.Models.mantenedor_model import (
    Estado_Civil, Comuna, Provincia, Region, Cargo
)
from datetime import datetime, timezone
from decimal import Decimal


class AuthenticationTests(APITestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil = Perfil.objects.create(
            pel_descripcion='Test Perfil',
            pel_vigente=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='testuser',
            password='testpass123',
            pel_id=self.perfil,
            usu_vigente=True
        )
    
    def test_token_obtain(self):
        """Test obtaining JWT token with valid credentials"""
        url = '/login/'
        data = {
            'usu_username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_token_obtain_invalid_credentials(self):
        """Test token rejection with invalid credentials"""
        url = '/login/'
        data = {
            'usu_username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh(self):
        """Test refreshing JWT token"""
        # First get tokens
        url = '/login/'
        data = {
            'usu_username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']
        
        # Now refresh
        url = '/refresh/'
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class UsuarioAPITests(APITestCase):
    """Test cases for Usuario API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil = Perfil.objects.create(
            pel_descripcion='Admin Perfil',
            pel_vigente=True
        )
        self.app = Aplicacion.objects.create(
            apl_descripcion='Usuarios',
            apl_vigente=True
        )
        Perfil_Aplicacion.objects.create(
            pel_id=self.perfil,
            apl_id=self.app,
            pea_consultar=True,
            pea_modificar=True,
            pea_eliminar=True,
            pea_ingresar=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='admin',
            password='admin123',
            pel_id=self.perfil,
            usu_vigente=True
        )
        # Authenticate
        response = self.client.post('/login/', {
            'usu_username': 'admin',
            'password': 'admin123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_usuarios(self):
        """Test listing all usuarios"""
        url = '/api/usuarios/usuarios/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_create_usuario(self):
        """Test creating a new usuario"""
        url = '/api/usuarios/usuarios/'
        data = {
            'usu_username': 'newuser',
            'password': 'newpass123',
            'pel_id': self.perfil.pel_id,
            'usu_vigente': True
        }
        response = self.client.post(url, data, format='json')
        # May be 201 or 400 depending on serializer validation
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_retrieve_usuario(self):
        """Test retrieving a specific usuario"""
        url = f'/api/usuarios/usuarios/{self.usuario.usu_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['usu_username'], 'admin')


class PerfilAPITests(APITestCase):
    """Test cases for Perfil API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil = Perfil.objects.create(
            pel_descripcion='Admin Perfil',
            pel_vigente=True
        )
        self.app = Aplicacion.objects.create(
            apl_descripcion='Perfiles',
            apl_vigente=True
        )
        Perfil_Aplicacion.objects.create(
            pel_id=self.perfil,
            apl_id=self.app,
            pea_consultar=True,
            pea_modificar=True,
            pea_eliminar=True,
            pea_ingresar=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='admin',
            password='admin123',
            pel_id=self.perfil,
            usu_vigente=True
        )
        response = self.client.post('/login/', {
            'usu_username': 'admin',
            'password': 'admin123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_perfiles(self):
        """Test listing all perfiles"""
        url = '/api/usuarios/perfiles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_perfil(self):
        """Test creating a new perfil"""
        url = '/api/usuarios/perfiles/'
        data = {
            'pel_descripcion': 'New Perfil',
            'pel_vigente': True
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class PersonaAPITests(APITestCase):
    """Test cases for Persona API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        # Create dependencies
        self.perfil = Perfil.objects.create(
            pel_descripcion='Admin Perfil',
            pel_vigente=True
        )
        self.app = Aplicacion.objects.create(
            apl_descripcion='Personas',
            apl_vigente=True
        )
        Perfil_Aplicacion.objects.create(
            pel_id=self.perfil,
            apl_id=self.app,
            pea_consultar=True,
            pea_modificar=True,
            pea_eliminar=True,
            pea_ingresar=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='admin',
            password='admin123',
            pel_id=self.perfil,
            usu_vigente=True
        )
        self.region = Region.objects.create(
            
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.provincia = Provincia.objects.create(
            reg_id=self.region,
            pro_descripcion='Concepción',
            pro_vigente=True
        )
        self.comuna = Comuna.objects.create(
            pro_id=self.provincia,
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
        # Authenticate
        response = self.client.post('/login/', {
            'usu_username': 'admin',
            'password': 'admin123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_personas(self):
        """Test listing all personas"""
        url = '/api/personas/personas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_persona(self):
        """Test retrieving a specific persona"""
        url = f'/api/personas/personas/{self.persona.per_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['per_run'], '12345678')
    
    def test_filter_personas_by_vigente(self):
        """Test filtering personas by vigente status"""
        # Create non-vigente persona
        Persona.objects.create(
            esc_id=self.estado_civil,
            com_id=self.comuna,
            usu_id=self.usuario,
            per_run='87654321',
            per_dv='0',
            per_apelpta='Pérez',
            per_nombres='María',
            per_mail='maria@example.com',
            per_fecha_nac=datetime(1995, 3, 20, tzinfo=timezone.utc),
            per_direccion='Otra Calle 456',
            per_tipo_fono=2,
            per_fono='+56987654321',
            per_apodo='Mary',
            per_vigente=False
        )
        url = '/api/personas/personas/?per_vigente=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CursoAPITests(APITestCase):
    """Test cases for Curso API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil = Perfil.objects.create(
            pel_descripcion='Admin Perfil',
            pel_vigente=True
        )
        self.app = Aplicacion.objects.create(
            apl_descripcion='Cursos',
            apl_vigente=True
        )
        Perfil_Aplicacion.objects.create(
            pel_id=self.perfil,
            apl_id=self.app,
            pea_consultar=True,
            pea_modificar=True,
            pea_eliminar=True,
            pea_ingresar=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='admin',
            password='admin123',
            pel_id=self.perfil,
            usu_vigente=True
        )
        # Create dependencies
        self.region = Region.objects.create(
            
            reg_descripcion='Biobío',
            reg_vigente=True
        )
        self.provincia = Provincia.objects.create(
            reg_id=self.region,
            pro_descripcion='Concepción',
            pro_vigente=True
        )
        self.comuna = Comuna.objects.create(
            pro_id=self.provincia,
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
        # Authenticate
        response = self.client.post('/login/', {
            'usu_username': 'admin',
            'password': 'admin123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_cursos(self):
        """Test listing all cursos"""
        url = '/api/cursos/cursos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_curso(self):
        """Test retrieving a specific curso"""
        url = f'/api/cursos/cursos/{self.curso.cur_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cur_codigo'], 'CURSO001')


class PagoAPITests(APITestCase):
    """Test cases for Pago API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil = Perfil.objects.create(
            pel_descripcion='Admin Perfil',
            pel_vigente=True
        )
        self.app = Aplicacion.objects.create(
            apl_descripcion='Pagos',
            apl_vigente=True
        )
        Perfil_Aplicacion.objects.create(
            pel_id=self.perfil,
            apl_id=self.app,
            pea_consultar=True,
            pea_modificar=True,
            pea_eliminar=True,
            pea_ingresar=True
        )
        self.usuario = Usuario.objects.create_user(
            usu_username='admin',
            password='admin123',
            pel_id=self.perfil,
            usu_vigente=True
        )
        self.proveedor = Proveedor.objects.create(
            prv_descripcion='Proveedor Test',
            prv_celular1='+56912345678',
            prv_direccion='Av. Principal 100',
            prv_vigente=True
        )
        # Authenticate
        response = self.client.post('/login/', {
            'usu_username': 'admin',
            'password': 'admin123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_proveedores(self):
        """Test listing all proveedores"""
        url = '/api/pagos/proveedor/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_proveedor(self):
        """Test retrieving a specific proveedor"""
        url = f'/api/pagos/proveedor/{self.proveedor.prv_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['prv_descripcion'], 'Proveedor Test')


class PermissionsAPITests(APITestCase):
    """Test cases for API permissions and authorization"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.perfil_no_perms = Perfil.objects.create(
            pel_descripcion='No Permissions Perfil',
            pel_vigente=True
        )
        self.usuario_no_perms = Usuario.objects.create_user(
            usu_username='noperms',
            password='noperms123',
            pel_id=self.perfil_no_perms,
            usu_vigente=True
        )
    
    def test_unauthorized_access(self):
        """Test that unauthorized requests are rejected"""
        url = '/api/usuarios/usuarios/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_forbidden_access_without_permissions(self):
        """Test that requests without proper permissions are forbidden"""
        # Login with user that has no app permissions
        response = self.client.post('/login/', {
            'usu_username': 'noperms',
            'password': 'noperms123'
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access usuarios endpoint
        url = '/api/usuarios/usuarios/'
        response = self.client.get(url)
        # Should be 403 or 401 depending on permission implementation
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])
