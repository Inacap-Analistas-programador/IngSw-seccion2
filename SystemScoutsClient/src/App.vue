<script setup>
import NavBar from './components/Reutilizables/NavBar.vue'
import SideBar from './components/Reutilizables/SideBar.vue';
</script>

<template>
		<div class="app-root">
			<NavBar />
			<main class="main-full">
				<router-view />
			</main>
		</div>
</template>

<style>
</style>
