<script setup>
import { ref } from 'vue'
import NavBar from './components/NavBar.vue'
import SideBar from './components/SideBar.vue'

const collapsed = ref(false)
function toggleCollapsed() {
	collapsed.value = !collapsed.value
}
</script>

<template>
	<div class="app-root">
		<NavBar :collapsed="collapsed" @toggle-sidebar="toggleCollapsed" />
		<div class="app-layout">
			<SideBar v-model:collapsed="collapsed" />
			<main class="main-content">
				<router-view v-slot="{ Component, route }">
					<Transition :name="route.meta.transition || 'fade'" mode="out-in">
						<component :is="Component" :key="route.path" />
					</Transition>
				</router-view>
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
	overflow: hidden;
}

.app-root {
	display: flex;
	flex-direction: column;
	height: 100vh;
}

.app-layout {
	display: flex;
	flex: 1;
}

.main-content {
	flex: 1;
	margin-left: var(--sidebar-width, 256px); /* Match sidebar width via variable */
	overflow-y: auto;
	padding: 16px; /* Restore padding for better spacing */
	background: #f5f5f5;
	position: relative;
	transition: margin-left 180ms ease; /* Smooth transition when sidebar collapses */
}

/* If the sibling sidebar is collapsed, reduce the main content margin */
.app-layout .sidebar.collapsed + .main-content {
	margin-left: var(--sidebar-collapsed-width, 70px);
}

/* Asegurarse de que la barra lateral ocupe toda la altura */
.sidebar {
	height: 100vh;
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
		margin-left: 0;
	}
}
</style>
