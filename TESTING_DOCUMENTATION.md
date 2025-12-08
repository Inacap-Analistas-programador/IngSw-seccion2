# Test Suite Documentation - Sistema de Scouts

Este documento describe la estrategia de testing implementada en el proyecto Sistema de Scouts.

## 📋 Tabla de Contenidos
1. [Arquitectura de Testing](#arquitectura-de-testing)
2. [Backend Testing (Django)](#backend-testing-django)
3. [Frontend Testing (Vue.js)](#frontend-testing-vuejs)
4. [Ejecución de Tests](#ejecución-de-tests)
5. [Cobertura de Código](#cobertura-de-código)
6. [CI/CD Integration](#cicd-integration)
7. [Best Practices](#best-practices)

---

## 🏗️ Arquitectura de Testing

### Niveles de Testing

1. **Unit Tests**: Pruebas de funciones, métodos y componentes aislados
2. **Integration Tests**: Pruebas de interacción entre módulos
3. **API Tests**: Pruebas de endpoints REST
4. **Manual QA**: Checklist de pruebas manuales (ver MANUAL_QA_CHECKLIST.md)

### Herramientas

#### Backend
- **Django Test Framework**: Framework nativo de Django
- **Django REST Framework Test**: Para pruebas de API
- **pytest** (opcional): Runner alternativo con mejores features
- **coverage.py**: Para reportes de cobertura

#### Frontend
- **Vitest**: Test runner rápido basado en Vite
- **Vue Test Utils**: Utilidades oficiales para testing de Vue
- **jsdom**: Simulación de entorno DOM

---

## 🔧 Backend Testing (Django)

### Estructura de Tests

```
SystemScoutsApi/
└── ApiCoreScouts/
    ├── tests/
    │   ├── __init__.py
    │   ├── test_models.py      # Tests de modelos Django
    │   └── test_api.py         # Tests de API REST
    └── tests.py                 # Importa todos los tests
```

### Tests de Modelos (`test_models.py`)

Prueban la lógica de negocio en los modelos:

- **UsuarioModelTest**: Creación, autenticación, validaciones
- **PerfilModelTest**: Perfiles y relación con aplicaciones
- **PersonaModelTest**: CRUD de personas, validación de RUN único
- **CursoModelTest**: Gestión de cursos, validación de código único
- **PagoModelTest**: Proveedores y pagos de personas

Ejemplo:
```python
def test_create_usuario(self):
    """Test creating a new Usuario"""
    usuario = Usuario.objects.create_user(
        usu_username='testuser',
        password='testpass123',
        pel_id=self.perfil
    )
    self.assertEqual(usuario.usu_username, 'testuser')
    self.assertTrue(usuario.check_password('testpass123'))
```

### Tests de API (`test_api.py`)

Prueban los endpoints REST:

- **AuthenticationTests**: Login, logout, refresh token
- **UsuarioAPITests**: CRUD de usuarios
- **PerfilAPITests**: Gestión de perfiles
- **PersonaAPITests**: CRUD de personas, filtros
- **CursoAPITests**: Gestión de cursos
- **PagoAPITests**: Gestión de pagos y proveedores
- **PermissionsAPITests**: Autorización y permisos

Ejemplo:
```python
def test_token_obtain(self):
    """Test obtaining JWT token with valid credentials"""
    url = '/token/'
    data = {
        'usu_username': 'testuser',
        'password': 'testpass123'
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
```

### Comandos de Ejecución

```bash
cd SystemScoutsApi

# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de un módulo específico
python manage.py test ApiCoreScouts.tests.test_models
python manage.py test ApiCoreScouts.tests.test_api

# Ejecutar un test específico
python manage.py test ApiCoreScouts.tests.test_models.UsuarioModelTest

# Con pytest (si está instalado)
pytest

# Con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML en htmlcov/
```

### Configuración pytest

El archivo `pytest.ini` define configuración para pytest:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = SystemScoutsApi.settings
python_files = tests.py test_*.py *_tests.py
testpaths = ApiCoreScouts/tests
```

---

## 🎨 Frontend Testing (Vue.js)

### Estructura de Tests

```
SystemScoutsClient/
└── src/
    ├── components/
    │   └── __tests__/
    │       ├── BaseButton.spec.js
    │       └── InputBase.spec.js
    └── services/
        └── __tests__/
            ├── authService.spec.js
            └── apiClient.spec.js
```

### Tests de Componentes

Prueban componentes Vue de forma aislada:

- **BaseButton.spec.js**: Renderizado, eventos, estados
- **InputBase.spec.js**: Input, validaciones, v-model

Ejemplo:
```javascript
it('renders button with text', () => {
  const wrapper = mount(BaseButton, {
    slots: {
      default: 'Click Me',
    },
  })
  expect(wrapper.text()).toContain('Click Me')
})
```

### Tests de Servicios

Prueban la lógica de servicios JavaScript:

- **authService.spec.js**: Login, logout, tokens
- **apiClient.spec.js**: HTTP requests, headers, error handling

Ejemplo:
```javascript
it('should store token on successful login', async () => {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ access: 'token' }),
  })
  
  const result = await authService.login('user', 'pass')
  expect(result).toHaveProperty('access')
})
```

### Comandos de Ejecución

```bash
cd SystemScoutsClient

# Instalar dependencias (primera vez)
npm install

# Ejecutar tests
npm run test

# Ejecutar tests en modo watch
npm run test -- --watch

# Ejecutar tests con UI interactiva
npm run test:ui

# Ejecutar tests con cobertura
npm run test:coverage

# Ejecutar test específico
npm run test -- BaseButton
```

### Configuración Vitest

El archivo `vitest.config.js` define la configuración:

```javascript
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
})
```

---

## 🚀 Ejecución de Tests

### Ejecución Local

#### Backend
```bash
cd SystemScoutsApi
venv\Scripts\activate
python manage.py test
```

#### Frontend
```bash
cd SystemScoutsClient
npm run test
```

### Ejecución en CI/CD

Los workflows de GitHub Actions ejecutan tests automáticamente:

- `.github/workflows/backend-ci.yml`: Tests de backend
- `.github/workflows/frontend-ci.yml`: Build de frontend
- `.github/workflows/code-quality.yml`: Linting y calidad

---

## 📊 Cobertura de Código

### Targets de Cobertura

- **Backend**: ≥ 80% (objetivo inicial: 60%)
- **Frontend**: ≥ 75% (cuando se completen todos los tests)

### Generar Reportes

#### Backend
```bash
cd SystemScoutsApi
coverage run --source='.' manage.py test
coverage report  # Reporte en consola
coverage html    # Reporte HTML en htmlcov/
```

#### Frontend
```bash
cd SystemScoutsClient
npm run test:coverage
# Reporte HTML en coverage/
```

### Interpretar Reportes

- **Verde (>80%)**: Buena cobertura
- **Amarillo (60-80%)**: Cobertura aceptable
- **Rojo (<60%)**: Requiere más tests

---

## 🔄 CI/CD Integration

### Backend CI Workflow

```yaml
# .github/workflows/backend-ci.yml
- name: Run tests
  run: |
    cd SystemScoutsApi
    python manage.py test
```

### Qué se Ejecuta

1. Setup de Python 3.12
2. Instalación de dependencias
3. Configuración de base de datos (SQLite para CI)
4. Ejecución de migraciones
5. Ejecución de tests

### Triggers

- Push a `main` o `develop`
- Pull requests a `main` o `develop`
- Cambios en `SystemScoutsApi/**` o `requirements.txt`

---

## ✅ Best Practices

### General

1. **Escribir tests antes o durante el desarrollo** (TDD/TBD)
2. **Un test, un concepto**: Cada test debe probar una sola cosa
3. **Nombres descriptivos**: `test_usuario_unique_username` mejor que `test1`
4. **Arrange-Act-Assert**: Estructura clara en cada test
5. **No dependencias entre tests**: Cada test debe ser independiente

### Backend

1. **Usar setUp y tearDown**: Para preparar datos de prueba
2. **Test de casos edge**: No solo happy path
3. **Mock de servicios externos**: Email, APIs externas
4. **Fixtures para datos complejos**: Reutilizar datos de prueba
5. **Test de permisos**: Verificar autorización en cada endpoint

### Frontend

1. **Mock de APIs**: No llamar al backend real
2. **Test de props y events**: Componentes como cajas negras
3. **Test de estados**: Loading, error, success
4. **Test de formularios**: Validaciones, submit
5. **Accesibilidad**: Test de atributos ARIA

### Ejemplos de Buenos Tests

#### Backend
```python
def test_persona_unique_run(self):
    """Test that RUN must be unique"""
    # Arrange: Create first persona
    Persona.objects.create(...)
    
    # Act & Assert: Try to create duplicate
    with self.assertRaises(IntegrityError):
        Persona.objects.create(per_run='12345678', ...)
```

#### Frontend
```javascript
it('emits update event on value change', async () => {
  // Arrange
  const wrapper = mount(InputBase, { props: { modelValue: '' }})
  
  // Act
  await wrapper.find('input').setValue('new value')
  
  // Assert
  expect(wrapper.emitted('update:modelValue')).toBeTruthy()
  expect(wrapper.emitted('update:modelValue')[0]).toEqual(['new value'])
})
```

---

## 🐛 Debugging Tests

### Backend

```bash
# Ejecutar con más verbosidad
python manage.py test --verbosity=2

# Ejecutar y mantener base de datos
python manage.py test --keepdb

# Ver traceback completo
python manage.py test --debug-mode
```

### Frontend

```bash
# Modo UI interactivo
npm run test:ui

# Con logs en consola
npm run test -- --reporter=verbose

# Ejecutar un solo test
npm run test -- -t "renders button"
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Django Testing](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)

### Guías del Proyecto

- [MANUAL_QA_CHECKLIST.md](./MANUAL_QA_CHECKLIST.md): Checklist de pruebas manuales
- [README.md](./README.md): Configuración del proyecto

---

## 🎯 Roadmap de Testing

### Corto Plazo (Completado)
- [x] Suite básica de tests de modelos
- [x] Tests de API para endpoints principales
- [x] Tests de autenticación
- [x] Configuración de pytest
- [x] Tests unitarios de componentes Vue
- [x] Tests de servicios frontend

### Mediano Plazo
- [ ] Aumentar cobertura a 80%+
- [ ] Tests de integración end-to-end
- [ ] Tests de performance
- [ ] Tests de carga

### Largo Plazo
- [ ] Tests automatizados de UI (Playwright/Cypress)
- [ ] Tests de accesibilidad
- [ ] Tests de seguridad automatizados
- [ ] Continuous testing en CI/CD

---

## 💡 Contribuir con Tests

Al agregar nueva funcionalidad:

1. **Escribir tests primero** (opcional pero recomendado)
2. **Agregar tests para la nueva feature**
3. **Asegurar que todos los tests pasen**
4. **Mantener/mejorar cobertura de código**
5. **Documentar casos especiales**

### Template de Test

```python
# Backend
def test_descripcion_clara(self):
    """Test description explaining what is being tested"""
    # Arrange: Setup test data
    
    # Act: Execute the code being tested
    
    # Assert: Verify the results
```

```javascript
// Frontend
it('descripción clara del test', () => {
  // Arrange: Setup
  
  // Act: Execute
  
  // Assert: Verify
})
```

---

**Nota**: Este documento está en constante evolución. Si encuentras áreas que necesitan más tests, por favor agrega issues o contribuye directamente.
