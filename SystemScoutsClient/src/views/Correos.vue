<template>
	<div class="correos-bg">
		<div class="correos-container">

				<PageHeader 
					title="Envío de Correos" 
					subtitle="Administra, crea y organiza los envíos de correo de formación." 
				/>

				<!-- Barra de filtros global -->
				<div class="filtros">
					<div class="filter-group">
						<FilterSelect 
							v-model="filters.curso" 
							:options="cursosOpts" 
							defaultLabel="Curso" 
						/>
					</div>

					<div class="filter-group">
						<FilterSelect 
							v-model="filters.rol" 
							:options="rolesOpts" 
							defaultLabel="Rol" 
						/>
					</div>

					<div class="filter-group">
						<FilterSelect 
							v-model="filters.estadoPersona" 
							:options="estadoPersonaOpts" 
							defaultLabel="Estado Persona" 
						/>
					</div>

					<div class="filter-group">
						<FilterSelect 
							v-model="filters.estadoCorreo" 
							:options="estadoCorreoOpts" 
							defaultLabel="Estado Correo" 
						/>
					</div>

					<div class="filter-actions">
						<BaseButton 
							class="search-button" 
							variant="primary" 
							@click="applyFilters"
							:disabled="!filters.curso || filters.curso === 'Todos'"
						>
							<AppIcons name="search" :size="16" />
						</BaseButton>
					</div>

					<!-- Botones de Acción movidos al header -->
				</div>

				<!-- Header estilo Mantenedor (Ubicado sobre la tabla) -->
				<div class="mantenedor-header">
					<div class="header-content">
						<h2><AppIcons name="map" :size="24" />Inscritos</h2>
						<div class="header-actions-group">
							<BaseButton class="header-icon-btn" variant="secondary" @click="exportarCorreos" title="Exportar Correos">
								<AppIcons name="download" :size="20" />
							</BaseButton>
							<BaseButton class="header-icon-btn" variant="primary" @click="marcarEnviado" :title="marcarButtonLabel">
								<AppIcons :name="marcarButtonIcon" :size="20" />
							</BaseButton>
							<BaseButton class="header-icon-btn" variant="primary" @click="enviarPorCorreo" title="Enviar por correo">
								<AppIcons name="send" :size="20" />
							</BaseButton>
						</div>
					</div>
				</div>

				<!-- Lista completa combinada -->
				<!-- Table Section Standardized -->
				<section class="table-section">
					<!-- Error Alert -->
					<div v-if="error" class="error-alert">
						<p>⚠️ {{ error }}</p>
					</div>

					<!-- Indicador de carga -->
					<div v-if="loading" class="loading-container">
						<div class="spinner"></div>
						<p>Cargando participantes...</p>
					</div>

					<div v-else class="table-container">
						<ModernMainScrollbar>
							<table class="data-table">
								<thead>
									<tr>
										<th style="width: 40px; text-align: center;">
											<input 
												type="checkbox" 
												v-model="allSelected" 
												:disabled="!rowsFiltered.length || seleccionIds.length === 0" 
												class="correos-checkbox"
											/>
										</th>
										<th>NOMBRE</th>
										<th>EMAIL</th>
										<th class="text-center">ESTADO PERSONA</th>
										<th class="text-center">ESTADO PAGO</th>
										<th class="text-center">ESTADO CORREO</th>
									</tr>
								</thead>
								<tbody>
									<tr v-if="!hasSearched">
										<td colspan="6" class="no-data-search">
											<div style="display: flex; flex-direction: column; align-items: center; gap: 12px;">
												<AppIcons name="info" :size="32" style="color: var(--primary); opacity: 0.8;" />
												<span style="font-weight: 500; color: var(--text-base);">Seleccione un CURSO para ver los participantes</span>
												<span style="font-size: 0.85em; opacity: 0.7;">Esto asegura que el estado de correo sea el correcto para el curso seleccionado.</span>
											</div>
										</td>
									</tr>
									<tr v-else-if="!rowsFiltered.length">
										<td colspan="6" class="no-data">No hay personas que coincidan con los filtros</td>
									</tr>
									<tr v-else v-for="row in rowsFiltered" :key="row.pecId || row.id">
										<td class="text-center" data-label="SELECCIÓN">
											<input 
												type="checkbox" 
												v-model="row.selected"
												:disabled="isRowDisabled(row)"
												class="correos-checkbox"
											/>
										</td>
										<td class="cell-name" data-label="NOMBRE"><span>{{ row.fullName }}</span></td>
										<td class="cell-email" data-label="EMAIL"><span>{{ row.email || '(sin email)' }}</span></td>
										<td class="text-center" data-label="ESTADO PERSONA">
											<span :class="['status-badge', vigenteClass(row)]">
												{{ row.vigente ? 'Vigente' : 'No vigente' }}
											</span>
										</td>
										<td class="text-center" data-label="ESTADO PAGO">
											<span :class="['status-badge', estadoPagoClass(row)]">
												{{ row.estadoPago }}
											</span>
										</td>
										<td class="text-center" data-label="ESTADO CORREO">
											<span :class="['status-badge', estadoCorreoClass(row)]">
												{{ row.estadoCorreo }}
											</span>
										</td>
									</tr>
								</tbody>
							</table>
						</ModernMainScrollbar>
					</div>

					<!-- Paginación (estilo Usuarios.vue) -->
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
</template>

<script setup>
import { reactive, computed, ref, onMounted } from 'vue'
import BaseButton from '../components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import NotificationToast from '@/components/NotificationToast.vue'
import ModernMainScrollbar from '@/components/ModernMainScrollbar.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import { personas as personasService, personaCursos as personaCursosService } from '@/services/personasService'
import { cursos as cursosService } from '@/services/cursosService'
import { rol } from '@/services/mantenedoresService'

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
const filters = reactive({ curso: null, rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })
// Filtros aplicados (se actualizan al presionar Buscar)
const appliedFilters = reactive({ curso: null, rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })

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

// Aplica los filtros al presionar el botón Buscar
function applyFilters() {
	if (!filters.curso || filters.curso === 'Todos') {
		notify('Debe seleccionar un curso obligatoriamente para buscar', 'alert-circle')
		return
	}
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
	}
	// Estado correo: si el usuario selecciona Enviado/Pendiente/No enviado, enviar pec_envio_correo_qr=1/0
	if (filters.estadoCorreo && filters.estadoCorreo !== 'Todos') {
		if (filters.estadoCorreo === 'Enviado') params.pec_envio_correo_qr = 1
		else if (filters.estadoCorreo === 'Pendiente' || filters.estadoCorreo === 'No enviado') params.pec_envio_correo_qr = 0
	}

	// Reset to first page when applying new filters
	page.value = 1
	// Save last query params (used when navigating pages)
	lastQueryParams.value = { ...params }
	// Fetch filtered rows from API
	fetchRows(params)
}

const seleccionIds = computed(() => rows.value.filter(r => r.selected).map(r => r.id))

function isRowDisabled(row) {
	if (row.selected) return false // deseleccionar siempre es posible
	const selRows = rows.value.filter(r => r.selected)
	if (selRows.length === 0) return false
	// Deshabilitar si el estado de correo es distinto al ya seleccionado
	return selRows[0].pecEnvioCorreoQR !== row.pecEnvioCorreoQR
}

const mostrarQR = ref(false)
const qrCanvas = ref(null)

// Opciones para los selects
const cursosOpts = ref([])
const rolesOpts = ref([])
const estadoPersonaOpts = ref([
	{ id: 'Todos', descripcion: 'Todos' },
	{ id: 'Vigente', descripcion: 'Vigente' },
	{ id: 'No vigente', descripcion: 'No vigente' }
])
const estadoCorreoOpts = ref([
	{ id: 'Todos', descripcion: 'Todos' },
	{ id: 'Enviado', descripcion: 'Enviado' },
	{ id: 'Pendiente', descripcion: 'Pendiente' },
	{ id: 'No enviado', descripcion: 'No enviado' }
])

// Cargar personas desde la API
async function fetchRows(params = {}) {
	hasSearched.value = true
	loading.value = true
	error.value = null
	try {
		const requestParams = { ...params }
		requestParams.page_size = 10000 
		
		if (appliedFilters.estadoCorreo === 'Enviado') requestParams.correo_qr_enviado = true
		else if (appliedFilters.estadoCorreo === 'Pendiente') requestParams.correo_qr_enviado = false
		
		if (appliedFilters.curso && appliedFilters.curso !== 'Todos') {
			requestParams.curso_descripcion = appliedFilters.curso
		}
		
		const personas = await personasService.paraCorreos(requestParams)
		
		let list = []
		if (Array.isArray(personas)) {
			list = personas
			total.value = personas.length
		} else if (personas && typeof personas === 'object') {
			if (Array.isArray(personas.results)) {
				list = personas.results
				total.value = personas.count ?? personas.total ?? list.length
			} else if (Array.isArray(personas.data)) {
				list = personas.data
				total.value = personas.count ?? personas.total ?? list.length
			} else {
				list = []
				total.value = 0
			}
		}

		rows.value = list.map(p => {
			// Helper para extraer campos con fallback de nombres (soporta snake_case, camelCase, UPPER_CASE)
			const get = (keys, fallback = '') => {
				for (const k of keys) {
					if (p[k] !== undefined && p[k] !== null) return p[k]
				}
				return fallback
			}

			const nombre = get(['nombre', 'per_nombres', 'PER_NOMBRES'])
			const apeP = get(['apellidoPaterno', 'per_apelpta', 'PER_APELPTA'])
			const apeM = get(['apellidoMaterno', 'per_apelmat', 'PER_APELMAT'])
			const email = get(['email', 'per_mail', 'per_email', 'PER_MAIL', 'PER_EMAIL'])
			const vigente = get(['vigente', 'per_vigente', 'PER_VIGENTE'], true)
			const pecId = get(['pec_id', 'pecId', 'PEC_ID'])
			const envCor = get(['pec_envio_correo_qr', 'pecEnvioCorreoQR', 'PEC_ENVIO_CORREO_QR'])
			const papEst = get(['pap_estado', 'papEstado', 'PAP_ESTADO'])
			const cursoDesc = get(['curso', 'CURSO', 'per_curso', 'PER_CURSO', 'cur_descripcion'])
			const rolDesc = get(['rol', 'ROL', 'per_rol', 'PER_ROL', 'rol_descripcion'])

			return {
				id: p.id || p.per_id || p.PER_ID,
				selected: false,
				pecId: pecId,
				pecEnvioCorreoQR: Boolean(envCor),
				nombre: nombre,
				apellidoPaterno: apeP,
				apellidoMaterno: apeM,
				email: email,
				curso: cursoDesc || 'Sin curso',
				rol: rolDesc || 'Participante',
				vigente: Boolean(vigente),
				estadoPersona: vigente ? 'Vigente' : 'No vigente',
				estadoPago: (papEst === 1 || papEst === true || papEst === '1') ? 'Pagado' : 'Pendiente',
				estadoCorreo: envCor ? 'Enviado' : 'Pendiente',
				fullName: `${apeP} ${apeM} ${nombre}`.trim()
			}
		})
		
		if (rows.value.length > 0) {
			console.log('Fila mapeada:', rows.value[0])
			console.log('Origen (RAW):', list[0])
		}

		total.value = rows.value.length
	} catch (e) {
		console.error('Error cargando personas:', e)
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
			rol.list()
		])

		const normalize = (val) => {
			if (!val) return []
			if (Array.isArray(val)) return val
			if (val && Array.isArray(val.data)) return val.data
			if (val && Array.isArray(val.results)) return val.results
			const keys = Object.keys(val || {})
			for (const k of keys) {
				if (Array.isArray(val[k])) return val[k]
			}
			return []
		}

		const cursosListRaw = normalize(cRes.status === 'fulfilled' ? cRes.value : null)
		if (cursosListRaw.length) {
			const cursosList = cursosListRaw.map(c => (
				(c && (c.CUR_DESCRIPCION || c.cur_descripcion || c.CUR_DESC)) || c.descripcion || c.nombre || c.titulo || c.title || c.name || c.curso || c.curso_nombre || c
			))
			const uniqueCursos = Array.from(new Set(cursosList)).filter(Boolean)
			cursosOpts.value = uniqueCursos.map(c => ({ id: c, descripcion: c }))
		}

		const rolesListRaw = normalize(rRes.status === 'fulfilled' ? rRes.value : null)
		if (rolesListRaw.length) {
			const rolesList = rolesListRaw.map(r => (r && (r.ROL_DESCRIPCION || r.rol_descripcion || r.ROL_DESC || r.descripcion)) || r.label || r.value || r).filter(Boolean)
			rolesOpts.value = Array.from(new Set(rolesList)).map(r => ({ id: r, descripcion: r }))
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
})

const rowsFiltered = computed(() => {
	let list = (rows.value || []).slice()
	if (appliedFilters.curso && appliedFilters.curso !== 'Todos') {
		const filterVal = String(appliedFilters.curso).toLowerCase().trim()
		list = list.filter(r => String(r.curso || '').toLowerCase().trim().includes(filterVal))
	}
	if (appliedFilters.rol && appliedFilters.rol !== 'Todos') {
		const filterVal = String(appliedFilters.rol).toLowerCase().trim()
		list = list.filter(r => String(r.rol || '').toLowerCase().trim().includes(filterVal))
	}
	if (appliedFilters.estadoPersona && appliedFilters.estadoPersona !== 'Todos') {
		if (appliedFilters.estadoPersona === 'Vigente') list = list.filter(r => Boolean(r.vigente))
		else if (appliedFilters.estadoPersona === 'No vigente') list = list.filter(r => !r.vigente)
	}
	return list
})

const allSelected = computed({
	get: () => {
		const visible = rowsFiltered.value
		if (!visible.length) return false
		return visible.every(r => r.selected)
	},
	set: (val) => {
		const visible = rowsFiltered.value
		if (val) {
			// Si ya hay algo seleccionado, buscamos su estado
			const selRows = rows.value.filter(r => r.selected)
			if (selRows.length > 0) {
				const targetStatus = selRows[0].pecEnvioCorreoQR
				visible.forEach(r => {
					if (r.pecEnvioCorreoQR === targetStatus) r.selected = true
				})
			} else {
				// Este caso no debería ocurrir si el checkbox está disabled
				// pero por seguridad, si no hay nada y los estados son consistentes, seleccionamos todo
				const firstRow = visible[0]
				const sameStatus = visible.every(r => r.pecEnvioCorreoQR === firstRow.pecEnvioCorreoQR)
				if (sameStatus) {
					visible.forEach(r => { r.selected = true })
				}
			}
		} else {
			visible.forEach(r => { r.selected = false })
		}
	}
})

const marcarButtonLabel = computed(() => {
	const sel = rows.value.filter(r => r.selected)
	if (!sel.length) return 'Marcar Enviado'
	const allSent = sel.every(t => Boolean(t.pecEnvioCorreoQR))
	return allSent ? 'Marcar Pendiente' : 'Marcar Enviado'
})

const marcarButtonIcon = computed(() => {
	const sel = rows.value.filter(r => r.selected)
	if (!sel.length) return 'check'
	const allSent = sel.every(t => Boolean(t.pecEnvioCorreoQR))
	return allSent ? 'circle-x' : 'check'
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
	if (np !== page.value) {
		page.value = np
		fetchRows(lastQueryParams.value || {})
	}
}

function onPageSizeChange() {
	page.value = 1
	fetchRows(lastQueryParams.value || {})
}

function vigenteClass(row) {
	return row.vigente ? 'status-active' : 'status-inactive'
}
function estadoPagoClass(row) {
	return row.estadoPago === 'Pagado' ? 'status-active' : 'badge-warning'
}
function estadoCorreoClass(row) {
	switch (row.estadoCorreo) {
		case 'Enviado': return 'status-active'
		case 'Pendiente': return 'badge-warning'
		case 'No enviado': return 'status-inactive'
		default: return 'badge-warning'
	}
}

function exportarCorreos() {
	const items = rows.value.filter(r => r.selected)
	const correos = items.map(i => i.email).filter(e => e).join(', ')
	if (!correos) {
		notify('Selecciona al menos un destinatario con correo', 'alert-circle')
		return
	}
	navigator.clipboard?.writeText(correos)
	notify('Correos copiados al portapapeles', 'clipboard')
}

async function marcarEnviado() {
	const toPersist = rows.value.filter(r => r.selected)
	if (!toPersist.length) {
		notify('Debe seleccionar al menos una persona', 'alert-circle')
		return
	}

	loading.value = true
	try {
		await Promise.all(toPersist.map(async t => {
			try {
				const current = Boolean(t.pecEnvioCorreoQR)
				const newVal = !current
				await personaCursosService.partialUpdate(t.pecId, { pec_envio_correo_qr: newVal })
				t.pecEnvioCorreoQR = newVal
				t.estadoCorreo = newVal ? 'Enviado' : 'Pendiente'
			} catch (err) {
				console.error(`Error actualizando persona ${t.id}:`, err)
			}
		}))
		notify('Estados actualizados correctamente', 'check')
		rows.value.forEach(r => { r.selected = false })
	} catch (err) {
		console.error('Error masivo marcarEnviado:', err)
		notify('Error al actualizar estados', 'alert-circle')
	} finally {
		loading.value = false
	}
}

function cerrarQR() {
	mostrarQR.value = false
}

async function enviarPorCorreo() {
	const selIds = seleccionIds.value
	if (!selIds.length) {
		notify('Selecciona al menos un registro', 'alert-circle')
		return
	}

	const subject = prompt('Asunto del correo:', 'Información del Curso')
	if (!subject) return

	const message = prompt('Mensaje del correo:', 'Estimado/a participante,\n\nTe enviamos la información del curso.')
	if (!message) return

	try {
		const correosService = (await import('@/services/correosService.js')).default
		const payload = { recipient_ids: selIds.map(id => Number(id)), subject, message }
		const result = await correosService.sendEmail(payload)

		for (const r of rows.value) {
			if (selIds.includes(r.id) && r.vigente && r.email) r.estadoCorreo = 'Enviado'
		}
		notify(`Envío completado. Enviados: ${result.sent}/${result.sent + result.failed}`, 'send')
	} catch (e) {
		console.error('Error enviando correos:', e)
		notify('No se pudieron enviar los correos', 'x-circle')
	}

	if (USE_BACKEND_ESTADO_CORREO) {
		try {
			const targets = rows.value.filter(r => r.selected && r.pecId)
			await Promise.all(targets.map(t => personaCursosService.partialUpdate(t.pecId, { PEC_ENVIO_CORREO_QR: true })))
		} catch (e) {
			console.error('No se pudo actualizar PEC_ENVIO_CORREO_QR:', e)
		}
	}
}
</script>

<style scoped>
/* Correos CSS Consolidated */
.correos-bg { height: 100%; width: 100%; }
.correos-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 24px;
  font-family: 'Inter', Arial, sans-serif;
  height: 100%;
  overflow: hidden;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .correos-container { 
    height: auto !important; 
    min-height: 100%;
    padding: 12px; 
    overflow: visible; 
  }
  .table-section {
    flex: none !important;
    overflow: visible !important;
    display: block;
    width: 100%;
  }
  .table-container { 
    height: auto !important;
    overflow: visible !important;
    border: none;
    background: transparent;
  }
  
  /* Transformation into cards */
  .data-table { 
    display: block !important;
    width: 100% !important;
    min-width: 0 !important; 
    background: transparent;
  }
  .data-table thead { display: none !important; }
  .data-table tbody { display: block !important; width: 100% !important; }
  
  .data-table tr { 
    display: block !important;
    width: 100% !important;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-bottom: 20px;
    padding: 12px 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .data-table td { 
    display: flex !important;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid #f1f5f9;
    text-align: right;
  }
  
  .data-table td:last-child { border-bottom: none; }
  
  .data-table td::before { 
    content: attr(data-label); 
    font-weight: 700; 
    color: #64748b; 
    text-transform: uppercase; 
    font-size: 0.75rem; 
    text-align: left; 
    flex: 0 0 130px; 
    margin-right: 8px;
  }
  
  .cell-name span, .cell-email span { 
    font-weight: 500;
    color: #1e293b;
  }
  
  .cell-name, .cell-email { text-align: right !important; }
  
  .mantenedor-header { 
    padding: 20px 0 10px; 
    text-align: center;
  }
  .header-content { flex-direction: column; gap: 12px; }
  .header-actions-group { width: 100%; justify-content: center; }
  .filtros { 
    justify-content: center; 
    padding-bottom: 20px; 
    gap: 12px;
  }
  .filter-group {
    flex: 1 1 100%; /* Individual rows on very small screens */
    width: 100%;
  }
}

.mantenedor-header { margin-bottom: 20px; padding: 32px 0px 16px; border-bottom: 2px solid #3949ab; }
.header-content { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.header-actions-group { display: flex; gap: 8px; }
.mantenedor-header h2 { color: #1a237e; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; margin: 0; }

.filtros { display: flex; align-items: flex-end; gap: 16px; flex-wrap: wrap; padding-bottom: 16px; margin-bottom: 16px; }
.filter-group { flex: 0 1 auto; display: flex; flex-direction: column; gap: 6px; }
.filtros label { font-weight: 600; color: var(--color-text); display: flex; align-items: center; gap: 8px; font-size: 0.9rem; margin-right: 0; }
.filtros select { padding: 5px 8px; border-radius: 6px; border: 1px solid var(--color-border); background: var(--color-surface); color: var(--color-text); min-width: 120px; font-size: 0.95rem; }

.table-section { width: 100%; display: flex; flex-direction: column; flex: 1; overflow: hidden}
.table-container { flex: 1; overflow: hidden; border-radius: 8px; }

.data-table { width: 100%; min-width: 800px; border-collapse: collapse; }
.data-table th, .data-table td { padding: 12px 15px; text-align: center; border-bottom: 1px solid #f0f0f0; }
.data-table th { background-color: #f8f9fa; color: #333; font-weight: 600; position: sticky; top: 0; z-index: 10; font-size: 0.85rem; text-transform: uppercase; }

.cell-name, .cell-email { text-align: left !important; }
.status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; }
.status-active { background-color: #e8f5e9; color: #2e7d32; }
.badge-warning { background-color: #fef3c7; color: #92400e; }
.status-inactive { background-color: #ffebee; color: #c62828; }
.correos-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #1a237e; }

.header-icon-btn, .search-button { height: 40px !important; width: 40px !important; padding: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; border-radius: 6px; }
.header-icon-btn :deep(svg), .search-button :deep(svg) { margin: 0 !important; }

.loading-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 1rem; gap: 1rem; color: #6b7280; font-weight: 500; }
.spinner { width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid var(--color-primary); border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.qr-modal { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.qr-modal-content { background: var(--color-surface); border-radius: 10px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); min-width: 280px; text-align: center; }
.qr-actions { margin-top: 15px; display:flex; justify-content:center; }
</style>