<script setup>
import { ref } from 'vue'
import NavBar from './components/NavBar.vue'
import SideBar from './components/SideBar.vue'
import ModernMainScrollbar from './components/ModernMainScrollbar.vue'

const collapsed = ref(false)
function toggleCollapsed() {
	collapsed.value = !collapsed.value
}

 
</script>

<template>
	<div class="app-root">
		<NavBar :collapsed="collapsed" @toggle-sidebar="toggleCollapsed" />
		<div class="app-layout" :class="{ 'is-collapsed': collapsed }">
			<SideBar :collapsed="collapsed" @update:collapsed="collapsed = $event" />
			<main class="main-content">
				<ModernMainScrollbar>
					<router-view v-slot="{ Component, route }">
						<Transition :name="route.meta.transition || 'fade'" mode="out-in">
							<!-- Use fullPath as key so components remount when query/hash/params change -->
							<!-- Use a composite key so remount triggers on name/params/query/hash changes -->
							<component :is="Component" :key="(route.name || route.path) + '|' + (route.fullPath || '')" />
						</Transition>
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
	background: #f5f5f5;
	position: relative;
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
