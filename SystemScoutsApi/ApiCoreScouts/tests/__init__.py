"""
Test suite for ApiCoreScouts
Exposes all test classes for Django test discovery
"""
from .test_models import (
    UsuarioModelTest,
    PerfilModelTest,
    ProveedorModelTest,
    MantenedorModelTest
)
from .test_api import (
    AuthenticationTests,
    UsuarioAPITests,
    PerfilAPITests,
    PersonaAPITests,
    CursoAPITests,
    PagoAPITests,
    PermissionsAPITests
)

__all__ = [
    'UsuarioModelTest',
    'PerfilModelTest',
    'ProveedorModelTest',
    'MantenedorModelTest',
    'AuthenticationTests',
    'UsuarioAPITests',
    'PerfilAPITests',
    'PersonaAPITests',
    'CursoAPITests',
    'PagoAPITests',
    'PermissionsAPITests',
]
