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
					<select v-model="filters.curso">
						<option value="Todos">Todos</option>
						<option v-for="c in cursos" :key="c" :value="c">{{ c }}</option>
					</select>
				</label>

				<label>
					Rol
					<select v-model="filters.cargo">
						<option value="Todos">Todos</option>
						<option value="Participante">Participante</option>
						<option value="Formador">Formador</option>
					</select>
				</label>

				<label>
					Estado de la persona
					<select v-model="filters.estadoPersona">
						<option value="Todos">Todos</option>
						<option value="Preinscrito">Preinscrito</option>
						<option value="Inscrito">Inscrito</option>
						<option value="Confirmado">Confirmado</option>
						<option value="Rechazado">Rechazado</option>
					</select>
				</label>

				<label>
					Estado de correo
					<select v-model="filters.estadoCorreo">
						<option value="Todos">Todos</option>
						<option value="Enviado">Enviado</option>
						<option value="Pendiente">Pendiente</option>
						<option value="No enviado">No enviado</option>
					</select>
				</label>

				<!-- Botón Buscar: aplica los filtros manualmente (al final de los filtros) -->
				<BaseButton variant="primary" @click="applyFilters" style="align-self: end; margin-left: 8px;">
					<AppIcons name="search" :size="16" /> Buscar
				</BaseButton>
			</div>

					<!-- Lista completa combinada -->
					<section class="correos-card">
						<div class="correos-card-header">
							<span class="correos-card-title blue-bar">Lista de Participantes</span>
							<div class="correos-card-actions">
								<BaseButton variant="secondary" @click="exportarCorreos"><AppIcons name="download" :size="16" /> Exportar Correos</BaseButton>
								<BaseButton variant="primary" @click="marcarEnviado"><AppIcons name="check" :size="16" /> Marcar Enviado</BaseButton>
								<BaseButton variant="primary" @click="enviarPorCorreo"><AppIcons name="send" :size="16" /> Enviar por correo</BaseButton>
							</div>
						</div>
						<div class="correos-card-desc">
							<span v-if="loading" style="color: var(--color-info); font-weight: 600;"> (Cargando...)</span>
							<span v-if="error" style="color: var(--color-danger); font-weight: 600;"> ⚠️ {{ error }}</span>
						</div>
						<div class="datatable-visual">
							<table class="datatable-table">
								<thead>
									<tr>
										<th></th>
										<th>Nombre</th>
										<th>Email</th>
										<th>Vigente</th>
										<th>Estado pago</th>
										<th>Estado persona</th>
										<th>Estado correo</th>
									</tr>
								</thead>
								<tbody>
									<tr v-if="loading">
										<td colspan="7" style="text-align: center; padding: 20px;">Cargando personas...</td>
									</tr>
									<tr v-else-if="error">
										<td colspan="7" style="text-align: center; padding: 20px; color: var(--color-danger);">{{ error }}</td>
									</tr>
									<tr v-else-if="!rowsFiltered.length">
										<td colspan="7" style="text-align: center; padding: 20px;">No hay personas que coincidan con los filtros</td>
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
											<span :class="['badge', estadoPersonaClass(row)]">
												{{ row.estadoPersona }}
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
import authViewsService from '@/services/auth_viewsService.js'
import { rol } from '@/services/mantenedoresService'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
// Flag temporal: cuando es false, 'Estado correo' NO se conecta a la API (sin PEC_ENVIO_CORREO_QR)
const USE_BACKEND_ESTADO_CORREO = false

// Datos desde la API
const rows = ref([])
const loading = ref(true)
const error = ref(null)

// Filtros editables (UI)
const filters = reactive({ curso: 'Todos', rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })
// Filtros aplicados (se actualizan al presionar Buscar)
const appliedFilters = reactive({ curso: 'Todos', rol: 'Todos', estadoPersona: 'Todos', estadoCorreo: 'Todos' })
// Aplica los filtros al presionar el botón Buscar
function applyFilters() {
	appliedFilters.curso = filters.curso
	appliedFilters.rol = filters.rol
	appliedFilters.estadoPersona = filters.estadoPersona
	appliedFilters.estadoCorreo = filters.estadoCorreo
}

const seleccion = reactive({})
const mostrarQR = ref(false)
const qrCanvas = ref(null)

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

// Cargar personas desde la API
onMounted(async () => {
	try {
		loading.value = true
		error.value = null

		let personas
		let cursosPersona = []
		if (USE_BACKEND_ESTADO_CORREO) {
			// Cargar personas y persona-curso en paralelo (tolerante a fallos del endpoint de cursos)
			const [pRes, cRes] = await Promise.allSettled([
				personasService.list(),
				personaCursosService.list()
			])
			if (pRes.status !== 'fulfilled') {
				throw pRes.reason || new Error('No se pudo cargar la lista de personas')
			}
			personas = pRes.value
			if (cRes.status === 'fulfilled') {
				cursosPersona = cRes.value
			} else {
				console.warn('No se pudieron cargar persona-curso:', cRes.reason)
				// Aviso no bloqueante
				notify('No se pudo cargar la relación persona-curso. Estado correo puede no reflejar backend.', 'alert-circle')
			}
		} else {
			// Temporalmente: sólo cargamos personas (estado correo se maneja localmente)
			personas = await personasService.list()
		}

		// Asegurarnos de que 'personas' es un array antes de usar .map.
		// La API puede devolver la lista directa, o un objeto con { data: [...] } / { results: [...] }.
		let list = []
		if (Array.isArray(personas)) {
			list = personas
		} else if (personas && Array.isArray(personas.data)) {
			list = personas.data
		} else if (personas && Array.isArray(personas.results)) {
			list = personas.results
		} else if (personas && Array.isArray(personas.personas)) {
			// Algunos endpoints devuelven un objeto con la lista en la clave 'personas'
			list = personas.personas
		} else {
			// Si recibimos un objeto inesperado, adjuntamos las keys para facilitar debug
			const keys = personas && typeof personas === 'object' ? Object.keys(personas) : []
			console.warn('Respuesta inesperada de personasService.list():', personas)
			throw new Error('Respuesta inesperada de la API de personas. Keys recibidas: ' + (keys.length ? keys.join(', ') : 'ninguna'))
		}

		// Mapa PER_ID -> registro Persona_Curso (sólo si está habilitado el backend para estado correo)
		let cursosMap = new Map()
		if (USE_BACKEND_ESTADO_CORREO && Array.isArray(cursosPersona)) {
			for (const c of cursosPersona) {
				const perId = c.PER_ID || (c.PER_ID_id ?? c.per_id) || c.perId || null
				if (!perId) continue
				if (!cursosMap.has(perId)) {
					cursosMap.set(perId, c)
				} else {
					const prev = cursosMap.get(perId)
					if (!prev.PEC_ENVIO_CORREO_QR && c.PEC_ENVIO_CORREO_QR) cursosMap.set(perId, c)
				}
			}
		}

		rows.value = list.map(p => ({
			id: p.id || p.PER_ID || null,
			pecId: (USE_BACKEND_ESTADO_CORREO ? (() => { const cp = cursosMap.get(p.PER_ID || p.id); return cp ? (cp.PEC_ID || cp.id || null) : null })() : null),
			pecEnvioCorreoQR: (USE_BACKEND_ESTADO_CORREO ? (() => { const cp = cursosMap.get(p.PER_ID || p.id); return cp ? (cp.PEC_ENVIO_CORREO_QR === true || cp.PEC_ENVIO_CORREO_QR === 1 || cp.PEC_ENVIO_CORREO_QR === '1') : false })() : false),
			// Normalizar posibles nombres de campo desde el backend
			nombre: p.PER_NOMBRES || p.nombre || p.nombre_completo || p.full_name || '',
			apellidoPaterno: p.PER_APELPTA || p.PER_APELLIDO_PATERNO || p.apellido_paterno || p.apellidoPaterno || p.apellido1 || '',
			apellidoMaterno: p.PER_APELMAT || p.PER_APELLIDO_MATERNO || p.apellido_materno || p.apellidoMaterno || p.apellido2 || '',
			email: p.PER_MAIL || p.email || p.mail || p.correo || '',
			curso: p.curso || 'Sin curso', // TODO: si viene desde persona-curso
			rol: p.rol || 'Participante', // TODO: desde relaciones
			// Estado de la persona (normalizado)
			estadoPersona: p.estadoPersona || p.estado || p.PER_ESTADO || 'Preinscrito',
			// Estado de pago (PAP_ESTADO): normalizar a Pagado / Pendiente
			estadoPagoRaw: p.PAP_ESTADO,
			estadoPagoBool: (p.PAP_ESTADO === 1 || p.PAP_ESTADO === true || p.PAP_ESTADO === '1'),
			estadoPago: (p.PAP_ESTADO !== undefined ? ((p.PAP_ESTADO === 1 || p.PAP_ESTADO === true || p.PAP_ESTADO === '1') ? 'Pagado' : 'Pendiente') : (p.estadoPago || 'Pendiente')),
			estadoCorreo: (USE_BACKEND_ESTADO_CORREO ? (() => { const s = cursosMap.get(p.PER_ID || p.id); return s && (s.PEC_ENVIO_CORREO_QR === true || s.PEC_ENVIO_CORREO_QR === 1 || s.PEC_ENVIO_CORREO_QR === '1') ? 'Enviado' : 'Pendiente' })() : 'Pendiente'),
			diasPendiente: null,
			// Normalizar campo 'vigente' que en el modelo es PER_VIGENTE
			vigente: (p.vigente !== undefined ? p.vigente : (p.PER_VIGENTE !== undefined ? p.PER_VIGENTE : true)) !== false,
			// nombre completo para mostrar en tabla (APELLIDO PATERNO + APELLIDO MATERNO + NOMBRES)
			fullName: [
				(p.PER_APELPTA || p.PER_APELLIDO_PATERNO || p.apellido_paterno || p.apellidoPaterno || ''),
				(p.PER_APELMAT || p.PER_APELLIDO_MATERNO || p.apellido_materno || p.apellidoMaterno || ''),
				(p.PER_NOMBRES || p.nombre || p.nombre_completo || p.full_name || '')
			].filter(Boolean).join(' ').trim()
		}))
		} catch (e) {
			// Si falla la petición a la API, mostrar el error y no usar mocks
			console.error('Error cargando personas desde API:', e)
			error.value = (e && e.message) ? e.message : String(e)
			rows.value = []
	} finally {
		loading.value = false
	}
})

const cursos = computed(() => {
	const s = new Set()
	rows.value.forEach(r => s.add(r.curso))
	return Array.from(s)
})

function matchesFilter(row) {
	if (appliedFilters.curso !== 'Todos' && row.curso !== appliedFilters.curso) return false
	if (appliedFilters.rol !== 'Todos' && row.rol !== appliedFilters.rol
		
	) return false
	if (appliedFilters.estadoPersona !== 'Todos' && row.estadoPersona !== appliedFilters.estadoPersona) return false
	if (appliedFilters.estadoCorreo !== 'Todos' && row.estadoCorreo !== appliedFilters.estadoCorreo) return false
	return true
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

const rowsFiltered = computed(() => {
	if (!rows.value) return []
	return rows.value.filter(matchesFilter)
})

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
	
	// Marca localmente como enviado
	for (const r of rows.value) {
		if (selIds.includes(String(r.id))) {
			r.estadoCorreo = 'Enviado'
		}
	}
	
		// Llamar al backend (servicio `auth_views`) para generar token firmado y persistirlo
		try {
			const payload = {
				ids: selIds.map(id => Number(id)),
				tipo: 'correo-enviado',
				expSeconds: 24 * 3600,
				usuId: 1 // TODO: usar usuario autenticado
			}
			const result = await authViewsService.qr_token(payload)
			const token = result && result.token

			// Renderizar QR con el token del backend
			if (!token) throw new Error('Respuesta inválida del servidor')
			mostrarQR.value = true
			await nextTick()
			await QRCode.toCanvas(qrCanvas.value, token, { width: 220 })
		} catch (e) {
			console.error('Error generando QR desde backend:', e)
			notify('No se pudo generar el QR: ' + (e?.message || e), 'x-circle')
		}

	// Persistir en backend PEC_ENVIO_CORREO_QR = true (si tenemos pecId) - sólo si está habilitado el backend
	if (USE_BACKEND_ESTADO_CORREO) {
		try {
			const targets = rows.value.filter(r => selIds.includes(String(r.id)) && r.pecId)
			await Promise.all(targets.map(t => personaCursosService.partialUpdate(t.pecId, { PEC_ENVIO_CORREO_QR: true })))
		} catch (e) {
			console.error('No se pudo actualizar PEC_ENVIO_CORREO_QR:', e)
			// Solo informar, ya que es una mejora de consistencia
			notify('No se pudo guardar el estado de correo en el servidor', 'alert-circle')
		}
	}
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

		try {
			const payload = {
				ids: selIds.map(id => Number(id)),
				tipo: 'correo-enviado',
				expSeconds: 24 * 3600,
				usuId: 1
			}
			const result = await authViewsService.qr_email(payload)

			// Marcar como enviados localmente
			for (const r of rows.value) {
				if (selIds.includes(String(r.id)) && r.vigente && r.email) {
					r.estadoCorreo = 'Enviado'
				}
			}

			notify(`Envío completado. Enviados: ${result.enviados}/${result.solicitados}`, 'send')
		} catch (e) {
			console.error('Error enviando correos:', e)
			notify('No se pudieron enviar los correos: ' + (e?.message || e), 'x-circle')
		}

	// Persistir en backend PEC_ENVIO_CORREO_QR = true (si tenemos pecId) - sólo si está habilitado el backend
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
	box-shadow: 0 4px 18px rgba(40,92,168,0.13);
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
	color: var(--color-primary);
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
	box-shadow: 0 2px 8px rgba(40,92,168,0.08);
	border: none;
	transition: all 0.3s ease;
}
.correos-card-actions button:hover {
	filter: brightness(0.95);
	box-shadow: 0 4px 16px rgba(40,92,168,0.13);
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
	background: var(--color-background-mute);
	color: var(--color-text);
	font-weight: 700;
	padding: 12px 10px;
	border-bottom: 2px solid var(--color-border);
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
	gap: 12px;
	align-items: center;
	justify-content: flex-start;
	margin: 10px auto 0 auto;
	/* Mismo ancho/gutter que el card */
	padding: 0 22px 12px 22px;
	flex-wrap: wrap;
	width: 100%;
	max-width: 1300px;
	box-sizing: border-box;
}
.filters-bar label {
	font-weight: 600;
	color: var(--color-text);
	display: flex;
	flex-direction: column;
	font-size: 0.95rem;
}
.filters-bar select {
	margin-top: 6px;
	padding: 6px 8px;
	border-radius: 6px;
	border: 1px solid var(--color-border);
	background: var(--color-surface);
	color: var(--color-text);
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
		padding: 0 8px 12px 8px;
		margin-left: 0;
		margin-right: 0;
		max-width: 100%;
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

 

