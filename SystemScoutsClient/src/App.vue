<script setup>
import NavBar from './components/NavBar.vue'
import SideBar from './components/SideBar.vue'
</script>

<template>
	<div class="app-root">
		<NavBar />
		<div class="app-layout">
			<SideBar />
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

body, html {
	height: 100%;
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
	margin-left: 250px; /* Ancho de la sidebar */
	overflow-y: auto;
	padding: 0; /* Eliminado el padding para que las vistas ocupen toda la pantalla */
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
		margin-left: 0;
	}
}
</style>
