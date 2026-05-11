<template>
  <div class="filtros">
    <div class="filter-group search-group">
      <SearchBar 
        :modelValue="tempSearchQuery" 
        @update:modelValue="$emit('update:tempSearchQuery', $event)"
        placeholder="Buscar por código o descripción..." 
        @search="$emit('aplicar')"
        class="search-bar-item"
      />
    </div>
    
    <div class="filter-group">
      <FilterSelect 
        :modelValue="filtros.estado" 
        @update:modelValue="$emit('update:filtros', { ...filtros, estado: $event })"
        :options="opcionesEstado" 
        defaultLabel="Estado" 
        valueKey="value"
        labelKey="text"
      />
    </div>
    <div class="filter-group">
      <FilterSelect 
        :modelValue="filtros.tipoCurso" 
        @update:modelValue="$emit('update:filtros', { ...filtros, tipoCurso: $event })"
        :options="tiposCursoOptions" 
        defaultLabel="Tipo Curso" 
        valueKey="value"
        labelKey="text"
        @focus="$emit('ensureCatalogo', 'tipos')" 
      />
    </div>
    <div class="filter-group">
      <FilterSelect 
        :modelValue="filtros.responsable" 
        @update:modelValue="$emit('update:filtros', { ...filtros, responsable: $event })"
        :options="personasOptions" 
        defaultLabel="Responsable" 
        valueKey="value"
        labelKey="text"
        @focus="$emit('ensureCatalogo', 'personas')" 
      />
    </div>

    <div class="filter-actions">
      <BaseButton 
        class="search-button" 
        variant="primary" 
        @click="$emit('aplicar')"
        :disabled="!hasAnyFilter"
      >
        <AppIcons name="search" :size="16" />
      </BaseButton>
      <BaseButton 
        class="search-button" 
        variant="secondary" 
        @click="$emit('limpiar')"
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

defineProps({
  filtros: Object,
  tempSearchQuery: String,
  opcionesEstado: Array,
  tiposCursoOptions: Array,
  personasOptions: Array,
  hasAnyFilter: Boolean
})

defineEmits(['update:filtros', 'update:tempSearchQuery', 'aplicar', 'limpiar', 'ensureCatalogo'])
</script>

<style scoped>
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
  min-width: 180px; 
}

.search-group {
  flex: 1 1 300px;
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

@media (max-width: 768px) {
  .filtros {
    padding: 16px;
    gap: 12px;
  }
}
</style>
