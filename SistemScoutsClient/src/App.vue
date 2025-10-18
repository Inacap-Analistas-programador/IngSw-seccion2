<template>
  <div id="app">
    <!-- Navbar importada -->
    <NavBar />

    <!-- Contenedor de las vistas según la ruta -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from '@/components/Reutilizables/NavBar.vue'
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}

main {
  padding: 2rem;
}
</style>
