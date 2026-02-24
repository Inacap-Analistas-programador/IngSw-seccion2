<script setup>
import { ref, onMounted, getCurrentInstance, computed } from 'vue'
import NavBar from './components/NavBar.vue'
import SideBar from './components/SideBar.vue'
import ModernMainScrollbar from './components/ModernMainScrollbar.vue'

const collapsed = ref(false)
const isPWA = ref(false)

function toggleCollapsed() {
	collapsed.value = !collapsed.value
}

onMounted(() => {
	// Detectar si estamos en modo PWA (standalone)
	if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
		isPWA.value = true
	}
})
</script>

<template>
	<div class="app-root" :class="{ 'is-pwa': isPWA }">
		<NavBar :collapsed="collapsed" @toggle-sidebar="toggleCollapsed" />
		<div class="app-layout" :class="{ 'is-collapsed': collapsed }">
			<SideBar :collapsed="collapsed" @update:collapsed="collapsed = $event" />
			<main class="main-content">
				<ModernMainScrollbar>
					<router-view v-slot="{ Component, route }">
						<component :is="Component" :key="(route.name || route.path) + '|' + (route.fullPath || '')" />
					</router-view>
				</ModernMainScrollbar>
			</main>
		</div>
	</div>
</template>

<style>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}
:root {
	--sidebar-width: 250px;
	--sidebar-collapsed-width: 70px;
}

body, html {
	height: 100%;
	/* Prevent global scrollbar so only main content scrolls */
	overflow: hidden;
}

.app-root {
	display: flex;
	flex-direction: column;
	height: 100vh;
	overflow: hidden;
}

.app-layout {
	display: flex;
	flex: 1;
	overflow: hidden;
}

.main-content {
	flex: 1;
	overflow-y: auto;
	padding: 16px;
	position: relative;
}

.full-width {
	width: 100% !important;
}

.no-sidebar .main-content {
	padding: 0; /* Verificador might want full bleed or specific padding */
}



/* ====== Animaciones de transición entre vistas ====== */

/* Fade básico (por defecto) */
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
	opacity: 0;
	transform: translateY(10px);
}

.fade-leave-to {
	opacity: 0;
	transform: translateY(-10px);
}

/* Slide desde la derecha */
.slide-left-enter-active,
.slide-left-leave-active {
	transition: all 0.3s ease;
}

.slide-left-enter-from {
	opacity: 0;
	transform: translateX(30px);
}

.slide-left-leave-to {
	opacity: 0;
	transform: translateX(-30px);
}

/* Slide desde la izquierda */
.slide-right-enter-active,
.slide-right-leave-active {
	transition: all 0.3s ease;
}

.slide-right-enter-from {
	opacity: 0;
	transform: translateX(-30px);
}

.slide-right-leave-to {
	opacity: 0;
	transform: translateX(30px);
}

/* Responsive: ocultar sidebar en móviles */
@media (max-width: 768px) {
	.main-content {
		margin-left: 0 !important;
	}
}
</style>
