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
								<BaseButton variant="primary">📧 Exportar Correos</BaseButton>
								<BaseButton variant="success">✅ Marcar Enviado</BaseButton>
							</div>
						</div>
						<div class="correos-card-desc">Lista completa — aplica filtros para reducir resultados</div>
						<div class="datatable-visual">
							<table class="datatable-table">
								<thead>
									<tr>
										<th></th>
										<th>Nombre</th>
										<th>Email</th>
										<th>Curso</th>
										<th>Cargo</th>
										<th>Pago</th>
										<th>Días Pend.</th>
										<th>Estado correo</th>
									</tr>
								</thead>
								<tbody>
									<tr v-for="row in rowsFiltered" :key="row.id">
										<td><input type="checkbox" /></td>
										<td class="cell-name">{{ row.nombre }}</td>
										<td class="cell-email">{{ row.email }}</td>
										<td>{{ row.curso }}</td>
										<td>{{ row.cargo }}</td>
										<td>{{ row.estadoPago }}</td>
										<td>{{ row.diasPendiente ?? '-' }}</td>
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
		</div>
	</div>
</template>


<script setup>
import { reactive, computed } from 'vue'
import BaseButton from '../components/Reutilizables/BaseButton.vue'

// Datos de ejemplo. En producción esto vendría desde la API.
const rowsCirculares = [
	{ id: 1, nombre: 'JUAN PÉREZ', email: 'juan.perez@email.com', curso: 'Formación', cargo: 'Participante', estadoPago: 'Pagado', estadoCorreo: 'Enviado' },
	{ id: 2, nombre: 'MARÍA GONZÁLEZ', email: 'maria.gonzalez@email.com', curso: 'Formación', cargo: 'Formador', estadoPago: 'Pendiente', estadoCorreo: 'Pendiente' },
	{ id: 4, nombre: 'ANA LÓPEZ', email: 'ana.lopez@email.com', curso: 'Taller', cargo: 'Participante', estadoPago: 'Pagado', estadoCorreo: 'Enviado' }
]

const rowsCobranza = [
	{ id: 3, nombre: 'CARLOS RAMÍREZ', email: 'carlos.ramirez@email.com', curso: 'Formación', cargo: 'Participante', estadoPago: 'Pendiente', estadoCorreo: 'No enviado', diasPendiente: '15 días' }
]

// Lista combinada
const rows = [...rowsCirculares, ...rowsCobranza]

const filters = reactive({ curso: 'Todos', cargo: 'Todos', estadoPago: 'Todos', estadoCorreo: 'Todos' })

const cursos = computed(() => {
	const s = new Set()
	rows.forEach(r => s.add(r.curso))
	return Array.from(s)
})

function matchesFilter(row) {
	if (filters.curso !== 'Todos' && row.curso !== filters.curso) return false
	if (filters.cargo !== 'Todos' && row.cargo !== filters.cargo) return false
	if (filters.estadoPago !== 'Todos' && row.estadoPago !== filters.estadoPago) return false
	if (filters.estadoCorreo !== 'Todos' && row.estadoCorreo !== filters.estadoCorreo) return false
	return true
}

const rowsFiltered = computed(() => rows.filter(matchesFilter))
</script>

<style scoped>
.correos-bg {
	min-height: 100vh;
	width: 100%;
	background: #ffffff;
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
	color: #285ca8;
	padding-left: 8px;
}
.correos-card {
	background: #fff;
	border-radius: 12px;
	box-shadow: 0 4px 18px rgba(40,92,168,0.13);
	margin: 0 auto 28px auto;
	padding: 22px 22px 16px 22px;
	max-width: 1300px;
	width: 100%;
	box-sizing: border-box;
	border: 1.5px solid #e3eaf6;
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
	color: #285ca8;
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
	background: #285ca8;
	border-radius: 4px;
}
.correos-card-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	width: 100%;
	max-width: 420px;
	justify-content: flex-end;
}
.correos-card-actions :deep(button),
.correos-card-actions button {
	min-width: 150px;
	font-size: 1rem;
	font-weight: 600;
	border-radius: 8px;
	box-shadow: 0 2px 8px rgba(40,92,168,0.08);
	border: none;
	transition: background 0.2s, box-shadow 0.2s;
}
.correos-card-actions :deep(.bg-blue-600),
.correos-card-actions button[variant="primary"] {
	background: linear-gradient(90deg, #3a8dde 0%, #6ec6ff 100%);
	color: #fff;
}
.correos-card-actions :deep(.bg-green-600),
.correos-card-actions button[variant="success"] {
	background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
	color: #fff;
}
.correos-card-actions :deep(.bg-yellow-400),
.correos-card-actions button[variant="warning"] {
	background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
	color: #333;
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
	background: #fafdff;
	border-radius: 10px;
	overflow: hidden;
	font-size: 1.05rem;
	margin-bottom: 0;
}
.datatable-table th {
	background: #e3eaf6;
	color: #123244; /* texto más oscuro para mejor contraste */
	font-weight: 700;
	padding: 12px 10px;
	border-bottom: 2px solid #b3c6e6;
	text-align: left;
}
.datatable-table td {
	padding: 12px 10px;
	border-bottom: 1px solid #e3eaf6;
	color: #122333; /* asegurar visibilidad del texto */
}
.datatable-table tr:nth-child(even) {
	background: #f4f6fb;
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
	box-shadow: 0 1px 4px rgba(40,92,168,0.07);
}
.badge-success {
	background: #e6f7e6;
	color: #1a7f37;
	border: 1px solid #b6e2c7;
}
.badge-warning {
	background: #fffbe6;
	color: #b8860b;
	border: 1px solid #ffe58f;
}
.badge-pending {
	background: #fff3e6;
	color: #b85c0b;
	border: 1px solid #ffd8b3;
}
input[type="checkbox"] {
	width: 18px;
	height: 18px;
	accent-color: #285ca8;
}
.filters-bar {
	display: flex;
	gap: 12px;
	align-items: center;
	margin: 10px 0 18px 0;
	flex-wrap: wrap;
}
.filters-bar label {
	font-weight: 600;
	color: #123244;
	display: flex;
	flex-direction: column;
	font-size: 0.95rem;
}
.filters-bar select {
	margin-top: 6px;
	padding: 6px 8px;
	border-radius: 6px;
	border: 1px solid #d7e3f5;
	background: #fff;
	color: #122333;
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
