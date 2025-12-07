<template>
	<ModernMainScrollbar>
		<div class="correos-bg">
			<div class="correos-container">
				<div class="page-header">
					<h3>Envío de Correos</h3>
					<p class="page-description">Administra, crea y organiza los envíos de correo de formación.</p>
				</div>

				<!-- Barra de filtros global -->
				<div class="filters-bar">
					<label>
						Curso
						<select v-model="filters.curso" class="compact-select">
							<option v-for="c in cursosOpts" :key="c" :value="c">{{ c }}</option>
						</select>
					</label>

					<label>
						Rol
						<select v-model="filters.rol" class="compact-select">
							<option v-for="r in rolesOpts" :key="r" :value="r">{{ r }}</option>
						</select>
					</label>

					<label>
						Estado persona
						<select v-model="filters.estadoPersona" class="compact-select">
							<option v-for="e in estadoPersonaOpts" :key="e" :value="e">{{ e }}</option>
						</select>
					</label>

					<label>
						Estado correo
						<select v-model="filters.estadoCorreo" class="compact-select">
							<option v-for="e in estadoCorreoOpts" :key="e" :value="e">{{ e }}</option>
						</select>
					</label>

					<BaseButton class="search-button" variant="primary" @click="applyFilters">
						<AppIcons name="search" :size="16" /> Buscar
					</BaseButton>
				</div>

				<!-- Lista completa combinada -->
				<section class="correos-card">
					<div class="correos-card-header">
						<span class="correos-card-title blue-bar">Lista de Participantes</span>
						<div class="correos-card-actions">
								<BaseButton variant="secondary" @click="exportarCorreos"><AppIcons name="download" :size="16" /> Exportar Correos</BaseButton>
								<BaseButton variant="primary" @click="marcarEnviado"><AppIcons name="check" :size="16" /> {{ marcarButtonLabel }}</BaseButton>
								<BaseButton variant="primary" @click="enviarPorCorreo"><AppIcons name="send" :size="16" /> Enviar por correo</BaseButton>
							</div>
					</div>
					<div class="correos-card-desc">
						<span v-if="error" style="color: var(--color-danger); font-weight: 600;"> ⚠️ {{ error }}</span>
					</div>

					<!-- Indicador de carga -->
					<div v-if="loading" class="loading-container">
						<div class="spinner"></div>
						<p>Cargando participantes...</p>
					</div>

					<div v-else class="datatable-visual">
						<table class="datatable-table">
							<thead>
								<tr>
									<th></th>
									<th>Nombre</th>
									<th>Email</th>
									<th>Vigente</th>
									<th>Estado pago</th>
									<th>Estado correo</th>
								</tr>
							</thead>
							<tbody>
								<tr v-if="!hasSearched">
									<td colspan="6" style="text-align: center; padding: 40px; color: var(--color-text-muted);">
										<div style="display: flex; flex-direction: column; align-items: center; gap: 12px;">
											<AppIcons name="search" :size="48" style="opacity: 0.5;" />
											<span>Seleccione filtros y presione <b>Buscar</b> para ver resultados</span>
										</div>
									</td>
								</tr>
								<tr v-else-if="error">
									<td colspan="6" style="text-align: center; padding: 20px; color: var(--color-danger);">{{ error }}</td>
								</tr>
								<tr v-else-if="!rowsFiltered.length">
									<td colspan="6" style="text-align: center; padding: 20px;">No hay personas que coincidan con los filtros</td>
								</tr>
								<tr v-else v-for="row in rowsFiltered" :key="row.id">
									<td><input type="checkbox" v-model="seleccion[row.id]" /></td>
									<td class="cell-name">{{ row.fullName }}</td>
									<td class="cell-email">{{ row.email || '(sin email)' }}</td>
									<td>
										<span :class="['badge', vigenteClass(row)]">
											{{ row.vigente ? 'Vigente' : 'No vigente' }}
										</span>
									</td>
									<td>
										<span :class="['badge', estadoPagoClass(row)]">
											{{ row.estadoPago }}
										</span>
									</td>
									<td>
										<span :class="['badge', estadoCorreoClass(row)]">
											{{ row.estadoCorreo }}
										</span>
									</td>
								</tr>
							</tbody>
						</table>
					</div>

					<!-- Paginación (estilo Usuarios.vue) -->
					<div class="pagination-bar">
						<div class="pagination-left">
							<label>Mostrar
								<select v-model.number="pageSize" @change="onPageSizeChange">
									<option v-for="s in pageSizes" :key="s" :value="s">{{ s }}</option>
								</select>
							</label>
							<span class="pagination-range">{{ showingRange }}</span>
						</div>
						<div class="pagination-right">
							<button class="pager-btn" :disabled="page === 1" @click="goToPage(page - 1)">Anterior</button>
							<template v-for="p in pagesToShow" :key="String(p) + '-' + page">
								<button v-if="p !== '...'" :class="['pager-btn', { active: p === page }]" @click="goToPage(p)">{{ p }}</button>
								<span v-else class="pager-ellipsis">…</span>
							</template>
							<button class="pager-btn" :disabled="page === totalPages" @click="goToPage(page + 1)">Siguiente</button>
						</div>
					</div>
				</section>

				<!-- Modal QR simple -->
				<div v-if="mostrarQR" class="qr-modal">
					<div class="qr-modal-content">
						<h3>Código QR generado</h3>
						<p>Escanea para verificar el envío</p>
						<canvas ref="qrCanvas"></canvas>
						<div class="qr-actions">
							<BaseButton variant="secondary" @click="cerrarQR">Cerrar</BaseButton>
						</div>
					</div>
				</div>

				<!-- Toast -->
				<NotificationToast v-if="showToast" :message="toastMessage" :icon="toastIcon" @close="showToast = false" />
			</div>
		</div>
	</ModernMainScrollbar>
</template>

<script setup>
import { reactive, computed, ref, onMounted, nextTick } from 'vue'
import BaseButton from '../components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import QRCode from 'qrcode'
import { personas as personasService, personaCursos as personaCursosService } from '@/services/personasService'
import { cursos as cursosService } from '@/services/cursosService'
import authViewsService from '@/services/auth_viewsService.js'
import { rol } from '@/services/mantenedoresService'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
// Flag temporal: cuando es true, 'Estado correo' se determina desde persona-cursos (PEC_ENVIO_CORREO_QR)
const USE_BACKEND_ESTADO_CORREO = true

// Datos desde la API
const rows = ref([])
const loading = ref(false)
const error = ref(null)
const hasSearched = ref(false)

// Paginación
const page = ref(1)
const pageSize = ref(50)
const pageSizes = [10, 25, 50, 100]
const total = ref(0)
const totalPages = computed(() => Math.max(1, Math.ceil((total.value || 0) / pageSize.value)))

// Guardar últimos parámetros de consulta para paginar sin perder filtros
const lastQueryParams = ref({})

// Filtros editables (UI)
const filters = reactive({ curso: 'Todos', rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })
// Filtros aplicados (se actualizan al presionar Buscar)
const appliedFilters = reactive({ curso: 'Todos', rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })
// Aplica los filtros al presionar el botón Buscar
function applyFilters() {
	// update appliedFilters for UI state
	appliedFilters.curso = filters.curso
	appliedFilters.rol = filters.rol
	appliedFilters.estadoPersona = filters.estadoPersona
	appliedFilters.estadoCorreo = filters.estadoCorreo

	// Build query params to send to backend (only non-'Todos')
	const params = {}
	if (filters.curso && filters.curso !== 'Todos') params.curso = filters.curso
	if (filters.rol && filters.rol !== 'Todos') params.rol = filters.rol
	// Estado persona: si el usuario selecciona 'Vigente' o 'No vigente', enviar per_vigente=1/0
	if (filters.estadoPersona && filters.estadoPersona !== 'Todos') {
		// backend persona filter expects parameter `vigente`
		if (filters.estadoPersona === 'Vigente') params.vigente = true
		else if (filters.estadoPersona === 'No vigente') params.vigente = false
		else params.estadoPersona = filters.estadoPersona
	}
	// Estado correo: si el usuario selecciona Enviado/Pendiente/No enviado, enviar pec_envio_correo_qr=1/0
	if (filters.estadoCorreo && filters.estadoCorreo !== 'Todos') {
		if (filters.estadoCorreo === 'Enviado') params.pec_envio_correo_qr = 1
		else if (filters.estadoCorreo === 'Pendiente' || filters.estadoCorreo === 'No enviado') params.pec_envio_correo_qr = 0
		else params.estadoCorreo = filters.estadoCorreo
	}

	// Reset to first page when applying new filters
	page.value = 1
	// Save last query params (used when navigating pages)
	lastQueryParams.value = { ...params }
	// Fetch filtered rows from API (page/page_size will be appended automatically)
	fetchRows(params)
}

const seleccion = reactive({})
const mostrarQR = ref(false)
const qrCanvas = ref(null)

// Opciones para los selects (provienen de la API)
const cursosOpts = ref(['Todos'])
const rolesOpts = ref(['Todos'])
// Estado persona ligado a PER_VIGENTE: 1 => Vigente, 0 => No vigente
const estadoPersonaOpts = ref(['Todos', 'Vigente', 'No vigente'])
const estadoCorreoOpts = ref(['Todos', 'Enviado', 'Pendiente', 'No enviado'])

// Toast de notificaciones
const showToast = ref(false)
const toastMessage = ref('')
const toastIcon = ref('')
function notify(msg, icon = '') {
	toastMessage.value = msg
	toastIcon.value = icon
	showToast.value = true
	// autocerrar suave en 4s
	setTimeout(() => { showToast.value = false }, 4000)
}

// Cargar personas desde la API (centralizado)
async function fetchRows(params = {}) {
	hasSearched.value = true
	loading.value = true
	error.value = null
	try {
		// attach pagination params
		const requestParams = { ...params }
		if (page.value) requestParams.page = page.value
		if (pageSize.value) requestParams.page_size = pageSize.value
		const personas = await personasService.list(requestParams)
		let cursosPersona = []
		if (USE_BACKEND_ESTADO_CORREO) {
			try {
				cursosPersona = await personaCursosService.list()
			} catch (e) {
				console.warn('No se pudieron cargar persona-curso (opcional):', e.message || e)
			}
		}

		// Normalize response and support paginated shapes ({count, results})
		let list = []
		if (Array.isArray(personas)) {
			list = personas
			total.value = personas.length
		} else if (personas && typeof personas === 'object') {
			// common paginated shapes: { count, results } or { total, data }
			if (Array.isArray(personas.results)) {
				list = personas.results
				total.value = personas.count ?? personas.total ?? list.length
			} else if (Array.isArray(personas.data)) {
				list = personas.data
				total.value = personas.count ?? personas.total ?? list.length
			} else if (Array.isArray(personas.personas)) {
				list = personas.personas
				total.value = personas.count ?? list.length
			} else {
				// fallback: try to find any array value inside
				const keys = Object.keys(personas)
				let found = false
				for (const k of keys) {
					if (Array.isArray(personas[k])) { list = personas[k]; found = true; break }
				}
				if (!found) {
					console.warn('Respuesta inesperada de personasService.list():', personas)
					throw new Error('Respuesta inesperada de la API de personas. Keys recibidas: ' + (keys.length ? keys.join(', ') : 'ninguna'))
				}
				total.value = list.length
			}
		} else {
			list = []
			total.value = 0
		}

		// Build map for persona-curso if available
		let cursosMap = new Map()
		if (USE_BACKEND_ESTADO_CORREO && Array.isArray(cursosPersona)) {
			for (const c of cursosPersona) {
				const perId = c.PER_ID || (c.PER_ID_id ?? c.per_id) || c.perId || null
				if (!perId) continue
				if (!cursosMap.has(perId)) cursosMap.set(perId, c)
				else {
					const prev = cursosMap.get(perId)
					if (!prev.PEC_ENVIO_CORREO_QR && c.PEC_ENVIO_CORREO_QR) cursosMap.set(perId, c)
				}
			}
		}

		rows.value = list.map(p => ({
			id: p.id || p.PER_ID || null,
			pecId: (USE_BACKEND_ESTADO_CORREO ? (() => { const cp = cursosMap.get(p.PER_ID || p.id); return cp ? (cp.PEC_ID || cp.id || null) : null })() : null),
			pecEnvioCorreoQR: (USE_BACKEND_ESTADO_CORREO ? (() => { const cp = cursosMap.get(p.PER_ID || p.id); return cp ? (cp.PEC_ENVIO_CORREO_QR === true || cp.PEC_ENVIO_CORREO_QR === 1 || cp.PEC_ENVIO_CORREO_QR === '1') : false })() : false),
			nombre: p.PER_NOMBRES || p.per_nombres || p.nombre || p.nombre_completo || p.full_name || '',
			apellidoPaterno: p.PER_APELPTA || p.per_apelpta || p.per_apelpat || p.PER_APELLIDO_PATERNO || p.apellido_paterno || p.apellidoPaterno || p.apellido1 || '',
			apellidoMaterno: p.PER_APELMAT || p.per_apelmat || p.PER_APELLIDO_MATERNO || p.apellido_materno || p.apellidoMaterno || p.apellido2 || '',
			email: p.PER_MAIL || p.per_mail || p.per_email || p.email || p.mail || p.correo || '',
			curso: p.curso || 'Sin curso',
			rol: p.rol || p.PER_ROL || 'Participante',
			// Mapear PER_VIGENTE (1/0/true/false) a labels y booleanos correctamente
			// Soportar varias formas que el backend pueda devolver (mayúsculas/minúsculas)
			_per_vigente_raw: (function() {
				if (p.PER_VIGENTE !== undefined) return p.PER_VIGENTE
				if (p.per_vigente !== undefined) return p.per_vigente
				if (p.vigente !== undefined) return p.vigente
				if (p.USU_VIGENTE !== undefined) return p.USU_VIGENTE
				return undefined
			})(),
			vigente: (function() {
				const raw = (function() {
					if (p.PER_VIGENTE !== undefined) return p.PER_VIGENTE
					if (p.per_vigente !== undefined) return p.per_vigente
					if (p.vigente !== undefined) return p.vigente
					if (p.USU_VIGENTE !== undefined) return p.USU_VIGENTE
					return undefined
				})()
				if (raw === undefined || raw === null) return true
				return (raw === 1 || raw === '1' || raw === true || raw === 'true')
			})(),
			estadoPersona: (function() {
				const raw = (function() {
					if (p.PER_VIGENTE !== undefined) return p.PER_VIGENTE
					if (p.per_vigente !== undefined) return p.per_vigente
					if (p.vigente !== undefined) return p.vigente
					if (p.USU_VIGENTE !== undefined) return p.USU_VIGENTE
					return undefined
				})()
				if (raw === undefined || raw === null) return (p.estadoPersona || p.estado || p.PER_ESTADO || 'Preinscrito')
				return (raw === 1 || raw === '1' || raw === true || raw === 'true') ? 'Vigente' : 'No vigente'
			})(),
			estadoPagoRaw: p.PAP_ESTADO,
			estadoPagoBool: (p.PAP_ESTADO === 1 || p.PAP_ESTADO === true || p.PAP_ESTADO === '1'),
			estadoPago: (p.PAP_ESTADO !== undefined ? ((p.PAP_ESTADO === 1 || p.PAP_ESTADO === true || p.PAP_ESTADO === '1') ? 'Pagado' : 'Pendiente') : (p.estadoPago || 'Pendiente')),
			estadoCorreo: (USE_BACKEND_ESTADO_CORREO ? (() => { const s = cursosMap.get(p.PER_ID || p.id); return s && (s.PEC_ENVIO_CORREO_QR === true || s.PEC_ENVIO_CORREO_QR === 1 || s.PEC_ENVIO_CORREO_QR === '1') ? 'Enviado' : 'Pendiente' })() : 'Pendiente'),
			diasPendiente: null,
			fullName: [
				(p.PER_APELPTA || p.per_apelpat || p.PER_APELLIDO_PATERNO || p.apellido_paterno || p.apellidoPaterno || ''),
				(p.PER_APELMAT || p.per_apelmat || p.PER_APELLIDO_MATERNO || p.apellido_materno || p.apellidoMaterno || ''),
				(p.PER_NOMBRES || p.per_nombres || p.nombre || p.nombre_completo || p.full_name || '')
			].filter(Boolean).join(' ').trim()
		}))

		// Si el filtro de Estado correo está activo y usamos el backend para derivarlo,
		// aplicar un filtrado cliente sobre PEC_ENVIO_CORREO_QR (0 = Pendiente, 1 = Enviado).
		if (appliedFilters.estadoCorreo && appliedFilters.estadoCorreo !== 'Todos' && USE_BACKEND_ESTADO_CORREO) {
			const wantSent = appliedFilters.estadoCorreo === 'Enviado'
			rows.value = rows.value.filter(r => Boolean(r.pecEnvioCorreoQR) === Boolean(wantSent))
			// Ajustar total para que la paginación muestre el rango correcto (cliente)
			total.value = rows.value.length
		}
	} catch (e) {
		console.error('Error cargando personas desde API:', e)
		error.value = (e && e.message) ? e.message : String(e)
		rows.value = []
	} finally {
		loading.value = false
	}
}

async function loadOptions() {
	try {
		const [cRes, rRes] = await Promise.allSettled([
			cursosService.list(),
			// obtener roles desde mantenedores para usar ROL_DESCRIPCION
			rol.list()
		])

		// Helper: normalizar distintas formas de respuesta a un array
		const normalize = (val) => {
			if (!val) return []
			if (Array.isArray(val)) return val
			if (val && Array.isArray(val.data)) return val.data
			if (val && Array.isArray(val.results)) return val.results
			// Algunas APIs devuelven { cursos: [...] }
			const keys = Object.keys(val || {})
			for (const k of keys) {
				if (Array.isArray(val[k])) return val[k]
			}
			return []
		}

		const cursosListRaw = normalize(cRes.status === 'fulfilled' ? cRes.value : null)
		if (cursosListRaw.length) {
			// Preferir CUR_DESCRIPCION del mantenedor de cursos si existe
			const cursosList = cursosListRaw.map(c => (
				(c && (c.CUR_DESCRIPCION || c.cur_descripcion || c.CUR_DESC)) || c.descripcion || c.nombre || c.titulo || c.title || c.name || c.curso || c.curso_nombre || c
			))
			cursosOpts.value = ['Todos', ...Array.from(new Set(cursosList)).filter(Boolean)]
		} else {
			console.warn('No se pudieron cargar cursos o respuesta vacía:', cRes.status === 'fulfilled' ? cRes.value : cRes.reason)
		}

		// Mapear roles desde la tabla mantenedores: usar ROL_DESCRIPCION
		const rolesListRaw = normalize(rRes.status === 'fulfilled' ? rRes.value : null)
		if (rolesListRaw.length) {
			rolesOpts.value = ['Todos', ...rolesListRaw.map(r => (r && (r.ROL_DESCRIPCION || r.rol_descripcion || r.ROL_DESC || r.descripcion)) || r.label || r.value || r).filter(Boolean)]
		} else {
			console.warn('No se pudieron cargar roles desde mantenedores o respuesta vacía:', rRes.status === 'fulfilled' ? rRes.value : rRes.reason)
		}

		// Usar PER_VIGENTE como fuente canonical: 1 => Vigente, 0 => No vigente
		estadoPersonaOpts.value = ['Todos', 'Vigente', 'No vigente']

		// Intentar derivar estadoCorreo desde personaCursos (PEC_ENVIO_CORREO_QR)
		try {
			const pcRes = await personaCursosService.list()
			const pcList = normalize(pcRes)
			if (pcList && pcList.length) {
				const estados = new Set()
				pcList.forEach(x => {
					const v = (x.PEC_ENVIO_CORREO_QR === true || x.PEC_ENVIO_CORREO_QR === 1 || x.PEC_ENVIO_CORREO_QR === '1') ? 'Enviado' : 'Pendiente'
					estados.add(v)
				})
				estadoCorreoOpts.value = ['Todos', ...Array.from(estados)]
			} else {
				estadoCorreoOpts.value = ['Todos', 'Enviado', 'Pendiente', 'No enviado']
			}
		} catch (e) {
			console.warn('No se pudieron derivar estados de correo desde personaCursos:', e)
			estadoCorreoOpts.value = ['Todos', 'Enviado', 'Pendiente', 'No enviado']
		}

	} catch (e) {
		console.warn('Error cargando opciones de filtros:', e)
	}
}

onMounted(async () => {
	loading.value = true
	await loadOptions()
	loading.value = false
	lastQueryParams.value = {}
	// await fetchRows() // No cargar al inicio, esperar a botón Buscar
})

const cursos = computed(() => {
	const s = new Set()
	rows.value.forEach(r => s.add(r.curso))
	return Array.from(s)
})

// Rows shown in the table: server may apply some filters, but provide
// a client-side layer so filters like `curso`, `rol` and `estadoPersona`
// work even if the API endpoint doesn't support them.
const rowsFiltered = computed(() => {
	let list = (rows.value || []).slice()
	// aplicar filtro por curso si está activo
	if (appliedFilters.curso && appliedFilters.curso !== 'Todos') {
		list = list.filter(r => String(r.curso || '').trim() === String(appliedFilters.curso).trim())
	}
	// aplicar filtro por rol si está activo
	if (appliedFilters.rol && appliedFilters.rol !== 'Todos') {
		list = list.filter(r => String(r.rol || '').trim() === String(appliedFilters.rol).trim())
	}
	// aplicar filtro por estadoPersona si está activo
	if (appliedFilters.estadoPersona && appliedFilters.estadoPersona !== 'Todos') {
		if (appliedFilters.estadoPersona === 'Vigente') list = list.filter(r => Boolean(r.vigente))
		else if (appliedFilters.estadoPersona === 'No vigente') list = list.filter(r => !r.vigente)
	}
	return list
})

// Etiqueta dinámica para el botón de marcar (según selección)
const marcarButtonLabel = computed(() => {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	if (!selIds.length) return 'Marcar Enviado'
	const targets = rows.value.filter(r => selIds.includes(String(r.id)))
	if (!targets.length) return 'Marcar Enviado'
	const allSent = targets.every(t => Boolean(t.pecEnvioCorreoQR))
	const allPending = targets.every(t => !t.pecEnvioCorreoQR)
	if (allSent) return 'Marcar Pendiente'
	if (allPending) return 'Marcar Enviado'
	return 'Alternar estado'
})

const startIndex = computed(() => {
	if (!total.value) return 0
	return (page.value - 1) * pageSize.value + 1
})
const endIndex = computed(() => {
	if (!total.value) return 0
	return Math.min(page.value * pageSize.value, total.value)
})

const showingRange = computed(() => {
	const t = total.value || 0
	if (t === 0) return '0-0 de 0'
	return `${startIndex.value}-${endIndex.value} de ${t}`
})

const pagesToShow = computed(() => {
	const tp = totalPages.value
	const current = page.value
	const out = []
	// If small number of pages, show all
	if (tp <= 9) {
		for (let i = 1; i <= tp; i++) out.push(i)
		return out
	}

	out.push(1)
	if (current > 4) out.push('...')

	const start = Math.max(2, current - 2)
	const end = Math.min(tp - 1, current + 2)
	for (let i = start; i <= end; i++) out.push(i)

	if (current < tp - 3) out.push('...')
	out.push(tp)
	return out
})

function goToPage(n) {
	if (!n || n < 1) return
	const np = Math.min(Math.max(1, n), totalPages.value)
	if (np === page.value) return
	page.value = np
	fetchRows(lastQueryParams.value || {})
}

function onPageSizeChange() {
	page.value = 1
	fetchRows(lastQueryParams.value || {})
}


// Clases de estilo para diferenciar visualmente los estados
function vigenteClass(row) {
	return row.vigente ? 'badge-success' : 'badge-danger'
}

function estadoPagoClass(row) {
	// Pagado: verde; Pendiente: amarillo
	return row.estadoPago === 'Pagado' ? 'badge-success' : 'badge-warning'
}

function estadoPersonaClass(row) {
	switch (row.estadoPersona) {
		case 'Confirmado':
			return 'badge-success'
		case 'Inscrito':
			return 'badge-warning'
		case 'Preinscrito':
			return 'badge-warning'
		case 'Rechazado':
			return 'badge-danger'
		default:
			return 'badge-warning'
	}
}

function estadoCorreoClass(row) {
	switch (row.estadoCorreo) {
		case 'Enviado':
			return 'badge-success'
		case 'Pendiente':
			return 'badge-warning'
		case 'No enviado':
			return 'badge-danger'
		default:
			return 'badge-warning'
	}
}

// rowsFiltered is server-driven (see above)

function exportarCorreos() {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	const items = rows.value.filter(r => selIds.includes(String(r.id)))
	const correos = items.map(i => i.email).filter(e => e).join(', ')
	if (!correos) {
		notify('Selecciona al menos un destinatario con correo', 'alert-circle')
		return
	}
	navigator.clipboard?.writeText(correos)
	notify('Correos copiados al portapapeles', 'clipboard')
}

async function marcarEnviado() {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	if (!selIds.length) {
		notify('Selecciona al menos un registro', 'alert-circle')
		return
	}

	const targets = rows.value.filter(r => selIds.includes(String(r.id)))
	if (!targets.length) return

	const toPersist = USE_BACKEND_ESTADO_CORREO ? targets.filter(t => t.pecId) : []
	const localOnly = targets.filter(t => !t.pecId || !USE_BACKEND_ESTADO_CORREO)

	let updated = 0
	let failed = 0

	// Persistir toggles en backend para los que tengan pecId
	if (toPersist.length) {
		try {
			await Promise.all(toPersist.map(async t => {
				try {
					const current = Boolean(t.pecEnvioCorreoQR)
					const newVal = !current
					await personaCursosService.partialUpdate(t.pecId, { PEC_ENVIO_CORREO_QR: newVal })
					// actualizar estado local
					t.pecEnvioCorreoQR = newVal
					t.estadoCorreo = newVal ? 'Enviado' : 'Pendiente'
					updated++
				} catch (err) {
					console.error('Error actualizando PEC for pecId', t.pecId, err)
					failed++
				}
			}))
		} catch (e) {
			console.error('Error en actualización de PEC_ENVIO_CORREO_QR:', e)
			notify('Error al actualizar estados en servidor', 'alert-circle')
		}
	}

	// Toggle local-only rows
	for (const t of localOnly) {
		const newVal = !t.pecEnvioCorreoQR
		t.pecEnvioCorreoQR = newVal
		t.estadoCorreo = newVal ? 'Enviado' : 'Pendiente'
	}

	// Notificar resultados
	const totalChanged = updated + localOnly.length
	if (failed > 0) notify(`Actualizados: ${totalChanged - failed}. Fallidos: ${failed}`, 'alert-circle')
	else notify(`Se actualizaron ${totalChanged} registros`, 'check')
}

function cerrarQR() {
	mostrarQR.value = false
}

async function enviarPorCorreo() {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	if (!selIds.length) {
		notify('Selecciona al menos un registro', 'alert-circle')
		return
	}

	// Open modal to compose email
	// For now, we'll use a simple prompt (you can enhance this with BaseModal later)
	const subject = prompt('Asunto del correo:', 'Información del Curso')
	if (!subject) return

	const message = prompt('Mensaje del correo:', 'Estimado/a participante,\n\nTe enviamos la información del curso.')
	if (!message) return

	// Get curso_id from filters if selected
	let cursoId = null
	if (filters.curso && filters.curso !== 'Todos') {
		// Find curso ID from cursoOptions
		const cursoOpt = cursoOptions.value.find(c => c.label === filters.curso || c.value === filters.curso)
		if (cursoOpt) cursoId = cursoOpt.value
	}

	try {
		const correosService = (await import('@/services/correosService.js')).default
		const payload = {
			recipient_ids: selIds.map(id => Number(id)),
			subject,
			message,
			...(cursoId && { curso_id: cursoId })
		}
		const result = await correosService.sendEmail(payload)

		// Mark as sent locally
		for (const r of rows.value) {
			if (selIds.includes(String(r.id)) && r.vigente && r.email) {
				r.estadoCorreo = 'Enviado'
			}
		}

		notify(`Envío completado. Enviados: ${result.sent}/${result.sent + result.failed}`, 'send')
	} catch (e) {
		console.error('Error enviando correos:', e)
		notify('No se pudieron enviar los correos: ' + (e?.message || e), 'x-circle')
	}

	// Persist in backend PEC_ENVIO_CORREO_QR = true (if we have pecId) - only if backend is enabled
	if (USE_BACKEND_ESTADO_CORREO) {
		try {
			const targets = rows.value.filter(r => selIds.includes(String(r.id)) && r.pecId)
			await Promise.all(targets.map(t => personaCursosService.partialUpdate(t.pecId, { PEC_ENVIO_CORREO_QR: true })))
		} catch (e) {
			console.error('No se pudo actualizar PEC_ENVIO_CORREO_QR:', e)
			notify('No se pudo guardar el estado de correo en el servidor', 'alert-circle')
		}
	}
}
</script>

<style scoped>
.correos-bg {
	min-height: 100vh;
	width: 100%;
	background: var(--color-background);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;
}
.correos-container {
	width: 100%;
	max-width: 1400px;
	margin: 0 auto;
	padding: 1.5rem;
}
.page-header { 
	margin-bottom: 2rem;
	padding-bottom: 1rem;
	border-bottom: 2px solid #e0e0e0;
}
.page-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.page-header p {
  font-size: 14px;
  color: #6b7280;
}
.page-description {
	margin: 0;
	font-size: 0.95rem;
	color: #7f8c8d;
	font-weight: 400;
}
/* eliminados estilos antiguos de título tipo banner y subtítulo azul */
.correos-card {
	background: var(--color-surface);
	border-radius: 12px;
	/* Shadow tuned to match Usuarios.vue subtle dark-blue neutral */
	box-shadow: 0 2px 8px rgba(16,24,40,0.06);
	margin: 0 auto 28px auto;
	padding: 22px 22px 16px 22px;
	max-width: 1300px;
	width: 100%;
	box-sizing: border-box;
	border: 1.5px solid var(--color-border);
}
.correos-card-header {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 10px;
	gap: 10px;
}
.correos-card-title {
	font-size: 1.18rem;
	font-weight: 700;
	/* Use same primary/title color as Usuarios.vue */
	color: #1e3a8a;
	position: relative;
	padding-left: 14px;
}
.blue-bar::before {
	content: '';
	position: absolute;
	left: 0;
	top: 0;
	height: 100%;
	width: 6px;
	background: var(--color-primary);
	border-radius: 4px;
}
.correos-card-actions {
	display: flex;
	flex-wrap: nowrap;
	gap: 12px;
	justify-content: flex-end;
}
.correos-card-actions :deep(button),
.correos-card-actions button {
	min-width: 160px;
	padding: 10px 16px;
	font-size: 1rem;
	font-weight: 600;
	border-radius: 8px;
	/* Subtle shadow similar to Usuarios actions */
	box-shadow: 0 2px 8px rgba(16,24,40,0.06);
	border: none;
	transition: all 0.3s ease;
}
.correos-card-actions button:hover {
	filter: brightness(0.95);
	box-shadow: 0 4px 16px rgba(16,24,40,0.08);
}
.correos-card-desc {
	color: #444;
	font-size: 1rem;
	margin-bottom: 10px;
}
.datatable-visual {
	width: 100%;
	overflow-x: auto;
}
.datatable-table {
	width: 100%;
	border-collapse: separate;
	border-spacing: 0;
	background: var(--color-background-soft);
	border-radius: 10px;
	overflow: hidden;
	font-size: 1.05rem;
	margin-bottom: 0;
}
.datatable-table th {
	/* Match Usuarios.vue table header colors */
	background: #3d4f5f;
	color: #ffffff;
	font-weight: 700;
	padding: 12px 10px;
	border-bottom: 2px solid rgba(0,0,0,0.06);
	text-align: left;
}
.datatable-table td {
	padding: 12px 10px;
	border-bottom: 1px solid var(--color-border);
	color: var(--color-text);
}
.datatable-table tr:nth-child(even) {
	background: var(--color-background-soft);
}
.datatable-table tr:last-child td {
	border-bottom: none;
}
.badge {
	display: inline-block;
	padding: 4px 14px;
	border-radius: 12px;
	font-size: 1em;
	font-weight: 600;
	letter-spacing: 0.5px;
	margin-right: 2px;
	box-shadow: 0 1px 4px rgba(0,0,0,0.08);
	border: 1px solid transparent;
}
.badge-success {
	background: var(--color-semaforo-green); /* Verde semáforo */
	color: #fff;
}
.badge-warning {
	background: var(--color-semaforo-yellow); /* Amarillo/naranja semáforo */
	color: #fff;
}
.badge-danger {
	background: var(--color-semaforo-red); /* Rojo semáforo */
	color: #fff;
}
.badge-secondary {
	background: #e9ecef;
	color: #334155;
	border-color: #cbd5e1;
}
.badge-soft-success {
	background: #d1f7d6; /* verde suave */
	color: #1a7f37;
	border-color: #95e0a2;
}
.badge-outline-warning {
	background: transparent;
	color: #b45309; /* ámbar oscuro */
	border-color: var(--color-semaforo-yellow);
}
.badge-striped {
	background-image: repeating-linear-gradient(-45deg, rgba(255,255,255,0.18) 0, rgba(255,255,255,0.18) 10px, transparent 10px, transparent 20px);
}
input[type="checkbox"] {
	width: 18px;
	height: 18px;
	accent-color: var(--color-primary);
}
.filters-bar {
	display: flex;
	gap: 10px;
	align-items: center;
	justify-content: flex-start;
	margin: 8px auto 0 auto;
	/* Mismo ancho/gutter que el card */
	padding: 6px 12px 8px 12px;
	flex-wrap: nowrap; /* mantener todo en una línea en pantallas grandes */
	overflow-x: auto; /* permitir scroll horizontal si no cabe */
	width: 100%;
	max-width: 1300px;
	box-sizing: border-box;
}
.filters-bar label {
    font-weight: 600;
    color: var(--color-text);
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    margin-right: 6px;
}
.filters-bar select {
    margin-top: 0;
    padding: 5px 8px;
    border-radius: 6px;
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    color: var(--color-text);
	min-width: 120px;
	max-width: 160px;
	font-size: 0.95rem;
}

/* Selects más compactos para estados (mismo look pero ocupando menos ancho) */
.filters-bar select.compact-select {
	min-width: 92px;
	max-width: 160px;
	padding: 4px 6px;
	font-size: 0.9rem;
}

/* Asegurar que el botón Buscar tenga la misma altura y estilo compacto */
.filters-bar :deep(.search-button) {
	display: inline-flex;
	align-items: center;
	height: 36px;
}
.filters-bar :deep(.search-button) button {
	height: 30px;
	padding: 6px 12px;
	font-size: 0.95rem;
}

.filters-bar .search-button {
	margin-left: 6px;
	align-self: center;
	flex: 0 0 auto;
}
@media (max-width: 900px) {
    .correos-title, .correos-subtitle, .correos-card {
		max-width: 100%;
		padding-left: 8px;
		padding-right: 8px;
	}
	.correos-card {
		padding: 8px 0 6px 0;
	}
	.filters-bar {
		padding: 6px 8px 10px 8px;
		margin-left: 0;
		margin-right: 0;
		max-width: 100%;
		gap: 8px;
		flex-wrap: wrap; /* permitir que envuelva en pantallas pequeñas */
	}
	.correos-card-actions {
		flex-direction: column;
		align-items: stretch;
		width: 100%;
		max-width: 100%;
		gap: 8px;
	}
	.datatable-table th, .datatable-table td {
		padding: 8px 4px;
		font-size: 0.97em;
	}
}

/* Pagination styles (copied from Usuarios.vue) */
.pagination-bar {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0 0 0;
	gap: 12px;
}
.pagination-left {
	display: flex;
	align-items: center;
	gap: 8px;
	color: #374151;
}
.pagination-left select {
	padding: 6px 8px;
	border-radius: 6px;
	border: 1px solid #e5e7eb;
	background: #fff;
}
.pagination-right .pager-btn {
	margin-left: 6px;
	padding: 6px 10px;
	border-radius: 8px;
	border: 1px solid rgba(16,24,40,0.06);
	background: #ffffff;
	box-shadow: 0 1px 2px rgba(16,24,40,0.04);
	cursor: pointer;
	color: #1f2937;
	transition: all 120ms ease;
}
.pagination-right .pager-btn:hover:not(:disabled) {
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(16,24,40,0.08);
}
.pagination-right .pager-btn.active {
	background: #1e40af;
	color: #fff;
	border-color: rgba(30,64,175,0.2);
}
.pagination-right .pager-btn:disabled {
	opacity: 0.45;
	cursor: not-allowed;
}
.pager-ellipsis {
	display: inline-block;
	margin: 0 6px;
	color: #6b7280;
	font-size: 1.1rem;
	vertical-align: middle;
}
.pagination-range {
	color: #6b7280;
	font-size: 0.9rem;
}

/* Loading Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  gap: 1rem;
  color: #6b7280;
  font-weight: 500;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

<style scoped>
.qr-modal {
	position: fixed;
	inset: 0;
	background: rgba(0,0,0,0.45);
	display: flex;
	align-items: center;
	justify-content: center;
}
.qr-modal-content {
	background: var(--color-surface);
	border-radius: 10px;
	padding: 16px 20px;
	box-shadow: 0 8px 20px rgba(0,0,0,0.2);
	min-width: 280px;
	text-align: center;
}
.qr-actions { margin-top: 10px; display:flex; justify-content:center; }
</style>

 

