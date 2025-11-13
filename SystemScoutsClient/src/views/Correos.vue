<template>
	<div class="correos-bg">
		<div class="correos-container">
			<h2 class="correos-subtitle">Gestión de Comunicaciones</h2>

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
					Cargo
					<select v-model="filters.cargo">
						<option value="Todos">Todos</option>
						<option value="Participante">Participante</option>
						<option value="Formador">Formador</option>
					</select>
				</label>

				<label>
					Estado de pago
					<select v-model="filters.estadoPago">
						<option value="Todos">Todos</option>
						<option value="Pagado">Pagado</option>
						<option value="Pendiente">Pendiente</option>
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
										<th>Curso</th>
										<th>Cargo</th>
										<th>Pago</th>
										<th>Estado correo</th>
									</tr>
								</thead>
								<tbody>
									<tr v-if="loading">
										<td colspan="8" style="text-align: center; padding: 20px;">Cargando personas...</td>
									</tr>
									<tr v-else-if="error">
										<td colspan="8" style="text-align: center; padding: 20px; color: var(--color-danger);">{{ error }}</td>
									</tr>
									<tr v-else-if="!rowsFiltered.length">
										<td colspan="8" style="text-align: center; padding: 20px;">No hay personas que coincidan con los filtros</td>
									</tr>
									<tr v-else v-for="row in rowsFiltered" :key="row.id">
										<td><input type="checkbox" v-model="seleccion[row.id]" /></td>
										<td class="cell-name">{{ row.nombre }}</td>
										<td class="cell-email">{{ row.email || '(sin email)' }}</td>
										<td>
											<span :class="['badge', row.vigente ? 'badge-success' : 'badge-pending']">
												{{ row.vigente ? 'Vigente' : 'No vigente' }}
											</span>
										</td>
										<td>{{ row.curso }}</td>
										<td>{{ row.cargo }}</td>
										<td>{{ row.estadoPago }}</td>
										<td>
											<span :class="['badge', row.estadoCorreo === 'Enviado' ? 'badge-success' : (row.estadoCorreo === 'Pendiente' ? 'badge-warning' : 'badge-pending')]">
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
		</div>
	</div>
</template>


<script setup>
import { reactive, computed, ref, onMounted, nextTick } from 'vue'
import BaseButton from '../components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'
import QRCode from 'qrcode'
import { personas as personasService } from '@/services/personasService'
import authViewsService from '@/services/auth_viewsService.js'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// Datos desde la API
const rows = ref([])
const loading = ref(true)
const error = ref(null)

const filters = reactive({ curso: 'Todos', cargo: 'Todos', estadoPago: 'Todos', estadoCorreo: 'Todos' })
const seleccion = reactive({})
const mostrarQR = ref(false)
const qrCanvas = ref(null)

// Cargar personas desde la API
onMounted(async () => {
	try {
		loading.value = true
		error.value = null
		const personas = await personasService.list()

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

		rows.value = list.map(p => ({
			id: p.id || p.PER_ID || null,
			// Normalizar posibles nombres de campo desde el backend
			nombre: p.nombre || p.nombre_completo || p.full_name || p.PER_NOMBRES || '',
			email: p.email || p.mail || p.correo || p.PER_MAIL || '',
			curso: p.curso || 'Sin curso', // TODO: si viene desde persona-curso
			cargo: p.cargo || 'Participante', // TODO: desde relaciones
			estadoPago: 'Pendiente', // TODO: enlazar pagos
			estadoCorreo: 'Pendiente',
			diasPendiente: null,
			// Normalizar campo 'vigente' que en el modelo es PER_VIGENTE
			vigente: (p.vigente !== undefined ? p.vigente : (p.PER_VIGENTE !== undefined ? p.PER_VIGENTE : true)) !== false
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
	if (filters.curso !== 'Todos' && row.curso !== filters.curso) return false
	if (filters.cargo !== 'Todos' && row.cargo !== filters.cargo) return false
	if (filters.estadoPago !== 'Todos' && row.estadoPago !== filters.estadoPago) return false
	if (filters.estadoCorreo !== 'Todos' && row.estadoCorreo !== filters.estadoCorreo) return false
	return true
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
		alert('Selecciona al menos un destinatario con correo')
		return
	}
	navigator.clipboard?.writeText(correos)
	alert('Correos copiados al portapapeles')
}

async function marcarEnviado() {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	if (!selIds.length) {
		alert('Selecciona al menos un registro')
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
			alert('No se pudo generar el QR: ' + e.message)
		}
}

function cerrarQR() {
	mostrarQR.value = false
}

async function enviarPorCorreo() {
	const selIds = Object.keys(seleccion).filter(k => seleccion[k])
	if (!selIds.length) {
		alert('Selecciona al menos un registro')
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

			alert(`✅ Envío completado\n\nSolicitados: ${result.solicitados}\nProcesados (vigentes con email): ${result.procesados}\nEnviados: ${result.enviados}\n\nRevisa la consola del servidor para ver los correos.`)
		} catch (e) {
			console.error('Error enviando correos:', e)
			alert('❌ No se pudieron enviar los correos: ' + e.message)
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
	padding: 16px 0 32px 0;
}
.correos-title {
	background: #285ca8;
	color: #fff;
	font-size: 1.6rem;
	font-weight: bold;
	border-radius: 10px 10px 0 0;
	padding: 16px 20px;
	margin: 0 0 12px 0;
	box-shadow: 0 2px 8px rgba(40,92,168,0.10);
}
.correos-subtitle {
	font-size: 1.25rem;
	font-weight: 600;
	margin: 0 0 18px 0;
	color: var(--color-primary);
	padding-left: 8px;
}
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
	padding: 4px 16px;
	border-radius: 14px;
	font-size: 1em;
	font-weight: 600;
	letter-spacing: 0.5px;
	margin-right: 2px;
	box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.badge-success {
	background: var(--color-semaforo-green); /* Verde semáforo */
	color: #fff;
	border: 1px solid transparent;
}
.badge-warning {
	background: var(--color-semaforo-yellow); /* Amarillo/naranja semáforo */
	color: #fff;
	border: 1px solid transparent;
}
.badge-pending {
	background: var(--color-semaforo-red); /* Rojo semáforo */
	color: #fff;
	border: 1px solid transparent;
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
	margin: 10px 0 0 0;
	padding: 0 8px 12px 50px;
	flex-wrap: wrap;
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

