<template>
  <section class="dashboard-grid">
    <!-- Iterar sobre filas -->
    <div
      v-for="(row, rowIndex) in dashboardRows"
      :key="rowIndex"
      class="dashboard-row"
    >
      <!-- Título de la fila (opcional) -->
      <h2 v-if="row.rowTitle" class="row-title">{{ row.rowTitle }}</h2>

      <!-- Contenedor de tarjetas en grilla -->
      <div class="row-cards">
        <DataCard
          v-for="(item, index) in row.items"
          :key="index"
          :title="item.title"
          :value="item.value"
          :description="item.description"
        >
          <!-- Icono opcional -->
          <template #icon v-if="item.icon">
            <i :class="item.icon"></i>
          </template>
        </DataCard>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue"
import DataCard from "./DataCard.vue"

const dashboardRows = ref([])

onMounted(async () => {
  try {
    dashboardRows.value = await fetchDashboardData()
  } catch (error) {
    console.error("Error cargando dashboard:", error)
  }
})
</script>

<style scoped>
.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.dashboard-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.row-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #19548a;
}

.row-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
</style>