<template>
  <div class="filtros">
    <div class="filter-group search-group">
      <SearchBar 
        v-model="searchQuery" 
        placeholder="Buscar por nombre, RUT, email..." 
        @search="$emit('search')"
        class="search-bar-item"
      />
    </div>
    
    <div class="filter-group">
      <FilterSelect 
        v-model="selectedRole" 
        :options="roleOptions" 
        defaultLabel="Rol" 
        valueKey="value"
        labelKey="label"
      />
    </div>
    <div class="filter-group">
      <FilterSelect 
        v-model="selectedGroup" 
        :options="groupOptions" 
        defaultLabel="Grupo" 
        valueKey="value"
        labelKey="label"
      />
    </div>
    <div class="filter-group">
      <FilterSelect 
        v-model="selectedEnrolledCourse" 
        :options="courseOptions" 
        defaultLabel="Curso" 
        valueKey="value"
        labelKey="label"
      />
    </div>
    <div class="filter-group">
      <FilterSelect 
        v-model="selectedRama" 
        :options="ramaOptions" 
        defaultLabel="Rama" 
        valueKey="value"
        labelKey="label"
      />
    </div>

    <div class="filter-actions">
      <BaseButton 
        class="search-button" 
        variant="primary" 
        @click="$emit('search')"
        :disabled="!hasAnyFilter"
      >
        <AppIcons name="search" :size="16" />
      </BaseButton>
      <BaseButton 
        class="search-button" 
        variant="secondary" 
        @click="$emit('clear')"
        title="Limpiar"
      >
        <AppIcons name="x-circle" :size="16" />
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import SearchBar from '@/components/common/SearchBar.vue'
import FilterSelect from '@/components/common/FilterSelect.vue'
import BaseButton from '@/components/BaseButton.vue'
import AppIcons from '@/components/icons/AppIcons.vue'

const props = defineProps({
  roleOptions: Array,
  groupOptions: Array,
  courseOptions: Array,
  ramaOptions: Array,
  hasAnyFilter: Boolean
})

const emit = defineEmits(['search', 'clear'])

const searchQuery = defineModel('searchQuery')
const selectedRole = defineModel('selectedRole')
const selectedGroup = defineModel('selectedGroup')
const selectedEnrolledCourse = defineModel('selectedEnrolledCourse')
const selectedRama = defineModel('selectedRama')
</script>

<style scoped>
/* Standardized structure matching CursoFilters.vue */
.filtros { 
  display: flex; 
  align-items: flex-end; 
  gap: 16px; 
  flex-wrap: wrap; 
  margin-bottom: 24px; 
}

.filter-group { 
  flex: 0 1 auto; 
  display: flex;
  flex-direction: row;
  gap: 6px; 
  min-width: 150px; 
}

.search-group {
  flex: 1 1 200px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  height: 42px;
}

.search-button { 
  height: 42px !important; 
  width: 42px !important; 
  padding: 0 !important; 
  display: flex !important; 
  align-items: center !important; 
  justify-content: center !important; 
  border-radius: 6px; 
}

.search-button :deep(svg) { margin: 0 !important; }

@media (max-width: 1024px) {
  .filtros {
    gap: 12px;
  }
  .filter-group, .search-group {
    flex: 1 1 100%;
    min-width: 0;
  }
  .filter-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
