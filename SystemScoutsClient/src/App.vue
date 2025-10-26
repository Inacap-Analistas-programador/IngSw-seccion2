<script setup>
import NavBar from './components/Reutilizables/NavBar.vue'
import SideBar from './components/Reutilizables/SideBar.vue';
</script>

<template>
	<div class="app-root">
		<NavBar />
		<div class="app-layout">
			<SideBar />
			<main class="main-content">
				<router-view />
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
	padding: 20px;
	background: #f5f5f5;
}

/* Responsive: ocultar sidebar en móviles */
@media (max-width: 768px) {
	.main-content {
		margin-left: 0;
	}
}
</style>
