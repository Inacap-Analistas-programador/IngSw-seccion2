<!-- DataCard.vue -->
<script setup>
// Se eliminan imports de macros innecesarios.
const props = defineProps({
  label: { type: String, required: true },
  modelValue: { type: Boolean, default: false },
});

const emit = defineEmits(["update:modelValue"]);

const handleChange = (event) => emit("update:modelValue", event.target.checked);
</script>

<template>
  <div class="p-4 bg-white shadow rounded-lg w-full max-w-sm">
    <label class="flex items-center space-x-2 cursor-pointer">
      <input
        type="checkbox"
        :checked="props.modelValue"
        @change="handleChange"
        class="w-5 h-5 rounded border-gray-400 text-blue-600 focus:ring focus:ring-blue-300"
      />
      <span class="text-gray-700">{{ props.label }}</span>
    </label>
  </div>
</template>

<style scoped>
/* Puedes agregar estilos extra aquí si quieres personalizar la tarjeta */
</style>
