<template>
  <nav class="bg-blue-600 text-white px-6 py-3 flex justify-between items-center shadow-md">
    <div class="flex items-center space-x-3">
      <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Scouts_de_Chile.png" 
           alt="Logo Scouts" 
           class="h-10 w-10" />
      <span class="text-lg font-bold">Scouts Biobío</span>
    </div>
    <ul class="hidden md:flex space-x-6">
      <li><a href="#" class="hover:text-yellow-300">Inicio</a></li>
      <li><a href="#" class="hover:text-yellow-300">Inscripciones</a></li>
      <li><a href="#" class="hover:text-yellow-300">Pagos</a></li>
      <li><a href="#" class="hover:text-yellow-300">Reportes</a></li>
    </ul>
    <!-- Menú móvil -->
    <button class="md:hidden bg-yellow-400 text-blue-800 px-3 py-1 rounded">
      ☰
    </button>
  </nav>
</template>

<script setup>
</script>

<style scoped>
/* Estilos opcionales */
</style>
