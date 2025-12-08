"""
Main test module for ApiCoreScouts
Imports all test cases from the tests package
"""
from django.test import TestCase

# Import all tests from the tests package
from .tests.test_models import (
    UsuarioModelTest,
    PerfilModelTest,
    ProveedorModelTest,
    MantenedorModelTest
)
from .tests.test_api import (
    AuthenticationTests,
    UsuarioAPITests,
    PerfilAPITests,
    PersonaAPITests,
    CursoAPITests,
    PagoAPITests,
    PermissionsAPITests
)

# All test classes are automatically discovered by Django's test runner
