# Running Tests - Sistema de Scouts

## Quick Start

### Backend Tests (Django)
```bash
cd SystemScoutsApi
pip install -r ../requirements.txt
python manage.py test
```

### Frontend Tests (Vue.js)
```bash
cd SystemScoutsClient
npm install
npm run test
```

## Backend Testing Details

### Prerequisites
- Python 3.12+
- Django 5.2+
- All requirements from `requirements.txt` installed

### Test Structure
- `ApiCoreScouts/tests/test_models.py` - Model tests
- `ApiCoreScouts/tests/test_api.py` - API endpoint tests  
- `ApiCoreScouts/tests.py` - Main test file (imports all tests)

### Running Tests

#### All Tests
```bash
python manage.py test
```

#### Specific Test Module
```bash
python manage.py test ApiCoreScouts.tests.test_models
python manage.py test ApiCoreScouts.tests.test_api
```

#### Specific Test Class
```bash
python manage.py test ApiCoreScouts.tests.test_models.UsuarioModelTest
python manage.py test ApiCoreScouts.tests.test_api.AuthenticationTests
```

#### Specific Test Method
```bash
python manage.py test ApiCoreScouts.tests.test_models.UsuarioModelTest.test_create_usuario
```

#### With Verbose Output
```bash
python manage.py test --verbosity=2
```

#### Keep Test Database (for debugging)
```bash
python manage.py test --keepdb
```

### Current Test Coverage

#### Model Tests (9 tests - ALL PASSING ✅)
- ✅ UsuarioModelTest (3 tests)
  - test_create_usuario
  - test_usuario_unique_username
  - test_usuario_password_hashing
- ✅ PerfilModelTest (2 tests)
  - test_create_perfil
  - test_perfil_aplicacion_relationship
- ✅ ProveedorModelTest (1 test)
  - test_create_proveedor
- ✅ MantenedorModelTest (3 tests)
  - test_create_estado_civil
  - test_create_region
  - test_create_cargo

#### API Tests  
- AuthenticationTests
- UsuarioAPITests
- PerfilAPITests
- PersonaAPITests
- CursoAPITests
- PagoAPITests
- PermissionsAPITests

## Frontend Testing Details

### Prerequisites
- Node.js 20+ 
- npm

### Test Structure
- `src/components/__tests__/` - Component tests
- `src/services/__tests__/` - Service tests

### Running Tests

#### All Tests
```bash
npm run test
```

#### Watch Mode
```bash
npm run test -- --watch
```

#### With Coverage
```bash
npm run test:coverage
```

#### UI Mode (Interactive)
```bash
npm run test:ui
```

#### Specific Test File
```bash
npm run test BaseButton
npm run test authService
```

### Current Test Coverage

#### Component Tests
- ✅ BaseButton.spec.js (6 tests)
- ✅ InputBase.spec.js (6 tests)

#### Service Tests
- ✅ authService.spec.js (6 tests)
- ✅ apiClient.spec.js (4 tests)

## Continuous Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### GitHub Actions Workflows
- `.github/workflows/backend-ci.yml` - Backend tests
- `.github/workflows/frontend-ci.yml` - Frontend build
- `.github/workflows/code-quality.yml` - Linting and quality checks

## Troubleshooting

### Backend

**Problem**: `ModuleNotFoundError: No module named 'django'`
```bash
# Solution: Install requirements
pip install -r requirements.txt
```

**Problem**: Database errors during tests
```bash
# Solution: Tests use SQLite by default (no MySQL needed)
# Make sure .env file has empty database settings
```

**Problem**: Import errors in tests
```bash
# Solution: Make sure you're in SystemScoutsApi directory
cd SystemScoutsApi
python manage.py test
```

### Frontend

**Problem**: `Cannot find module 'vitest'`
```bash
# Solution: Install dependencies
npm install
```

**Problem**: Tests fail with DOM errors
```bash
# Solution: jsdom should be installed automatically
# If not: npm install --save-dev jsdom
```

## Writing New Tests

### Backend Test Example
```python
from django.test import TestCase
from ApiCoreScouts.Models.usuario_model import Usuario, Perfil

class MyModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.perfil = Perfil.objects.create(
            pel_descripcion='Test',
            pel_vigente=True
        )
    
    def test_something(self):
        """Test description"""
        # Arrange
        usuario = Usuario.objects.create_user(
            usu_username='test',
            password='test123',
            pel_id=self.perfil
        )
        
        # Act & Assert
        self.assertEqual(usuario.usu_username, 'test')
```

### Frontend Test Example
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '../MyComponent.vue'

describe('MyComponent', () => {
  it('renders correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.text()).toContain('Expected Text')
  })
})
```

## Additional Resources

- [TESTING_DOCUMENTATION.md](./TESTING_DOCUMENTATION.md) - Comprehensive testing guide
- [MANUAL_QA_CHECKLIST.md](./MANUAL_QA_CHECKLIST.md) - Manual testing checklist
- [Django Testing Docs](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Vitest Documentation](https://vitest.dev/)
