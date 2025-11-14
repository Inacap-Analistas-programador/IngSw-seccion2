// Central service barrel file
// Import services here and re-export them so views can import from a single path.
// This makes future refactors (rename/remove services) much easier.

import * as apiClient from './apiClient'
import * as authService from './authService'
import * as authViewsService from './auth_viewsService'
import * as personasService from './personasService'
import * as usuariosService from './usuariosService'
import * as cursosService from './cursosService'
import * as mantenedoresService from './mantenedoresService'
import * as pagosService from './pagosService'
import * as archivosService from './archivosService'
import * as reportesService from './reportesService'
// usuariosRolesService and CorreosService are legacy files removed after migration
// dashboardService removed — functionality split into per-section services (cursos, pagos, personas, etc.)

// Export everything as named exports. Prefer importing from '@/services' in views.
export {
  apiClient,
  authService,
  authViewsService,
  personasService,
  usuariosService,
  // Removed legacy usuariosRolesService,
  cursosService,
  mantenedoresService,
  pagosService,
  archivosService,
  reportesService,
  // Removed legacy CorreosService,
}

// Backwards-compat aliases (safe to import old names from this barrel):
export const personas = personasService.personas || personasService
export const usuarios = usuariosService.usuarios || usuariosService
export const reportes = reportesService

// NOTE: Once views are migrated to import from specific new services
// you can safely remove legacy files like `CorreosService.js` or `usuariosRolesService.js`.
